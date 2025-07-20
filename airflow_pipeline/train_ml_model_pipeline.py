from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def task1_load_clean(**context):
    value = "Hello from Task1!"
    # load data from flights.csv files
    df = pd.read_csv('/media/sudip/linux-extra/code/almabetter/prodmlsys/data/flights.csv')
    flights = df.drop_duplicates()
    flights_data = flights[['flightType', 'price', 'distance', 'time','agency']]
    context['ti'].xcom_push(key='flights_data', value=flights_data.to_dict(orient='records'))
    
    print(f"Task1 pushed value:")


def task2__transform_and_train(**context):
   
    # Print the value received from Task1
    flights_data = context['ti'].xcom_pull(task_ids='load_data_and_clean', key='flights_data')
    # Convert the list of dictionaries back to a DataFrame
    flights_df = pd.DataFrame(flights_data)
    print(flights_df.head())

    X = flights_df.drop('price', axis=1)
    Y= flights_df['price']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    flightType_encoder = LabelEncoder()
    agency_encoder = LabelEncoder()

    X_train['flightType_encoded'] = flightType_encoder.fit_transform(X_train['flightType'])
    X_train['agency_encoded'] = agency_encoder.fit_transform(X_train['agency'])

    X_test['flightType_encoded'] = flightType_encoder.transform(X_test['flightType'])
    X_test['agency_encoded'] = agency_encoder.transform(X_test['agency'])

    # Drop original categorical columns
    X_train = X_train.drop(['flightType', 'agency'], axis=1)
    X_test = X_test.drop(['flightType', 'agency'], axis=1)  

    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, Y_train)  


        # get the fitted ecoder and model
    joblib.dump(flightType_encoder, 'flightType_encoder.pkl')
    print("FlightType encoder saved as flightType_encoder.pkl")
    joblib.dump(agency_encoder, 'agency_encoder.pkl')
    print("Agency encoder saved as agency_encoder.pkl")
    joblib.dump(rf_model, 'rf_model_best.pkl')
    print("Model saved as rf_model_best.pkl")

    print(f"Task2 received value:")


with DAG(
    dag_id='train_ml_model_pipeline_dag',
    default_args=default_args,
    description='Load data from csv files, clean it, split into train and test sets, and train a model',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    
    task1 = PythonOperator(
        task_id='load_data_and_clean',
        python_callable=task1_load_clean,
        multiple_outputs=True
    )   

    # Define Task2
    task2 = PythonOperator(
        task_id='split_transform_and_train',
        python_callable=task2__transform_and_train,
   
    )

    # Set the sequence: Task1 >> Task2
    task1 >> task2

# Instructions:
# 1. Save this file as airflow_dag.py in your Airflow DAGs folder (e.g., ~/airflow/dags/).
# 2. Start the Airflow scheduler and webserver:
#      airflow scheduler &
#      airflow webserver -p 8080
# 3. In the Airflow UI (http://localhost:8080), enable and trigger 'example_xcom_dag'.
# 4. Monitor Task1 and Task2 logs to see the XCom push and pull messages.
