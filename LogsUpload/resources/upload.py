import json
import boto3
import os
import datetime

bucket_name = os.environ['BUCKET']

# Use boto3 to interact with S3
s3_client = boto3.client("s3")

print(bucket_name)

def handler(event,context):
    # Extract day, month, and year to build the path
    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    path = str(year) + "-" + str(month) + "/" + str(day)

    print(current_time)
    print(event)
    
    # Get the request body
    request_body = json.loads(event["body"])
    # Extract data from the request body (modify based on your needs)
    data_to_store = request_body["data"]
    print("***********************************",data_to_store)
    
    # Store the data in S3 (modify bucket name and key)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"cdk/{path}/{current_time}aws.log",  # Replace with appropriate key structure
        Body=str(data_to_store)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data stored successfully!"})
    }

# 
# 
# from botocore.exceptions import ClientError

# s3 = boto3.client('s3')
# bucket_name = os.environ['BUCKET']

# def lambda_handler(event, context):
#     print(event)
#     try:
#         method = event['httpMethod']
#         widget_name = event['pathParameters'].get('proxy')

#         if method == "GET":
#             if event['path'] == "/":
#                 print(" **** GET: Path: / **** ")
#                 data = s3.list_objects_v2(Bucket=bucket_name)
#                 body = {
#                     "widgets": [obj['Key'] for obj in data['Contents']]
#                 }
#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps(body)
#                 }

#             if widget_name:
#                 print(" **** GET: Path: /widget_name **** ")

#                 data = s3.get_object(Bucket=bucket_name, Key=widget_name)
#                 body = data['Body'].read().decode('utf-8')
#                 return {
#                     'statusCode': 200,
#                     'body': json.dumps(body)
#                 }

#         if method == "POST":
#             if not widget_name:
#                 return {
#                     'statusCode': 400,
#                     'body': "Widget name missing"
#                 }

#             now = str(datetime.datetime.now())
#             data = widget_name + " created: " + now
#             s3.put_object(Bucket=bucket_name, Key=widget_name, Body=data.encode('utf-8'), ContentType='application/json')
#             return {
#                 'statusCode': 200,
#                 'body': data
#             }

#         if method == "DELETE":
#             if not widget_name:
#                 return {
#                     'statusCode': 400,
#                     'body': "Widget name missing"
#                 }

#             s3.delete_object(Bucket=bucket_name, Key=widget_name)
#             return {
#                 'statusCode': 200,
#                 'body': "Successfully deleted widget " + widget_name
#             }

#         return {
#             'statusCode': 400,
#             'body': "We only accept GET, POST, and DELETE, not " + method
#         }

#     except ClientError as e:
#         return {
#             'statusCode': 400,
#             'body': e.response['Error']['Message']
#         }
#     except Exception as e:
#         return {
#             'statusCode': 400,
#             'body': str(e)
#         }