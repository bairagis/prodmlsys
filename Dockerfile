# Dockerfile to install all requirements.txt and build predict_flight_price_api and run this flask app

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code

COPY . .

# Expose the port Flask runs on
EXPOSE 5002

# Set environment variables for Flask
ENV FLASK_APP=predict_flight_price_api.py
ENV FLASK_RUN_HOST=0.0.0.0

# Free port 5002 if any process is using it
RUN apt-get update && apt-get install -y lsof && \
    lsof -ti:5002 | xargs --no-run-if-empty kill || true

# Run the Flask app
CMD ["python", "api/predict_flight_price_api.py"]