import json
import boto3
import os
import datetime

bucket_name = os.environ['BUCKET']

# Use boto3 to interact with S3
s3_client = boto3.client("s3")

def handler(event,context):
    # Extract day, month, and year to build the path
    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    path = str(year) + "-" + str(month) + "/" + str(day)
    
    # Get the request body
    try:
        body = json.loads(event['body'])
        #get userId to add to key
        userId = body["userId"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)+": Requred filed missing"
        }
        
    #get log info
    try:
        data_to_store=body["log"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)+": Requred filed missing"
        }
    #s3 upload
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"cdk/{path}/{userId}/{current_time}.aws.log",  
            Body=str(data_to_store)
        )
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)+": Fail wo write to s3"
        }
        
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data stored successfully!"})
    }
