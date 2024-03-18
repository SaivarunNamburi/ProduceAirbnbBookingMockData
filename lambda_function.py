import uuid
import random
from datetime import datetime, timedelta
import boto3
import json
import os

sqs_client = boto3.client('sqs')
QUEUE_URL = os.environ.get('AWS_SQS_ARN')
# List of example cities and countries
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
countries = ["USA"]

def generate_mock_data():
    
    booking_id = str(uuid.uuid4())
    user_id = random.randint(1000, 9999)
    property_id = random.randint(100, 999)
    location = random.choice(cities) + ", " + random.choice(countries)
    start_date = datetime.now() + timedelta(days=random.randint(1, 365))
    end_date = start_date + timedelta(days=random.randint(1, 30))
    price = round(random.uniform(50, 5000), 2)
    return {
        "bookingId": booking_id,
        "userId": user_id,
        "propertyId": property_id,
        "location": location,
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "price": price
    }

def lambda_handler(event, context):
    i = 0
    while (i < 30):
        sales_order = generate_mock_data()
        print(sales_order)
        sqs_client.send_message(
            QueueURL = QUEUE_URL,
            MessageBody = json.dumps(sales_order)
        )
        i += 1

    return {
        'statusCode' : 200,
        'body' : json.dumps('Sales order data has been published in SQS')
    }

