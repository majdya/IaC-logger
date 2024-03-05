import json
import boto3
import os
import datetime
import urllib.parse
import gzip
import io

dest = os.environ['DEST']

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

    print(current_time,": S3 Trigger!!!")
    
    # Extract the bucket name from the S3 event
    bkt = event['Records'][0]['s3']['bucket']['name']
    # Extract the object key from the S3 event and decode it
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    print("Bucket:", bkt)
    print("Key:", key)
    print("dest:", dest)
    
    to_compress = s3_client.get_object(Bucket=bkt, Key=key)
    # Read the contents of the object
    object_content = to_compress['Body'].read()
    print("pre-decode:", object_content)

    compressed_stream = io.BytesIO()
    
    with gzip.GzipFile(fileobj=compressed_stream, mode='wb') as f:
        # Write the payload to the compressed file
        f.write(object_content)
    
    compressed_data = compressed_stream.getvalue()
    
    s3_client.put_object(
        Bucket=dest,
        # Replace with appropriate key structure
        Key=f"compressed/{key}",
        Body=compressed_data
        )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data stored successfully!"})
    }