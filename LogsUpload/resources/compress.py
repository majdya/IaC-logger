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

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(current_time,": S3 Trigger!!!")
    
    # Extract the bucket name from the S3 event
    bkt = event['Records'][0]['s3']['bucket']['name']
    # Extract the object key from the S3 event and decode it
    try:
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    except Exception as e:
        print(e)
    try:    
        to_compress = s3_client.get_object(Bucket=bkt, Key=key)
        # Read the contents of the object
        object_content = to_compress['Body'].read()
        # Compress the contents of the object
        compressed_stream = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_stream, mode='wb') as f:
            # Write the payload to the compressed file
            f.write(object_content)

    except Exception as e:
        print("Fail to Compress file!!")
        print(e)
    
    compressed_data = compressed_stream.getvalue()
    
    try:
        s3_client.put_object(
            Bucket=dest,
            Key=f"compressed/{key}",
            Body=compressed_data
            )
    except Exception as e:
        print("Fail to write to S3")
        print(e)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data stored successfully!"})
    }