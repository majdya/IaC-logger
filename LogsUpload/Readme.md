# Log Upload Service

## Overview

The Log Upload Service handles the storage of log data in an S3 bucket.

## Components

### 1. `log_upload_service/log_upload_service_stack.py`:

This code defines an AWS CDK stack for the Log Upload Service.
Here's a breakdown of the components:

1. **Imports**:

   - `Construct` is imported from the `constructs` module.
   - `Stack` is imported from `aws_cdk`.
   - The `log_upload_service` module is imported.

1. **LogUploadServiceStack Class**:

   - This class extends `Stack` and is responsible for defining the infrastructure stack for the Log Upload Service.

1. **Constructor**:

   - The constructor method initializes the LogUploadServiceStack and accepts the `scope`, `construct_id`, and `kwargs`.

1. **Initialization**:
   - The `LogUploadService` from the `log_upload_service` module is instantiated within the stack, with the identifier "LogUpload".

This code essentially sets up the AWS CDK stack for the Log Upload Service, allowing the infrastructure for log uploading to be defined and deployed using AWS CDK.

---

### 2.`log_upload_service/log_upload_service.py`:

This code defines an AWS CDK (Cloud Development Kit) construct for the Log Upload Service. It creates an API Gateway, Tow S3 buckets, and Lambda functions to handle log uploads and compression.
Here's a breakdown of the components:

1. **S3 Buckets**:
   Two S3 buckets named "UploadHandler" and "CompressHandler" are created to store the uploaded logs and compressed data, respectively.

2. **Lambda Functions**:

   - `uploadHandler`: A Lambda function that handles the upload of log data to the "UploadHandler" S3 bucket.
   - `compressHandler`: A Lambda function that handles the compression of log data and stores it in the "CompressHandler" S3 bucket.

3. **API Gateway**:

   - An API Gateway named "upload-api" is created to serve the uploaded logs.

4. **Integration**:

   - The `uploadHandler` Lambda function is integrated with the API Gateway to handle POST requests for log uploads.
   - The `compressHandler` Lambda function is granted read access to the "UploadHandler" bucket and read/write access to the "CompressHandler" bucket.

5. **S3 Event Notification**:
   - A Lambda event notification is added to the "UploadHandler" bucket to trigger the `compressHandler` function when new objects are created.

### 3.`resources/upload.py`:

This Python function serves as an AWS Lambda handler for processing API Gateway requests. Here's a breakdown of the code:

1. **Imports**:

   - `json`, `boto3`, `os`, and `datetime` are imported to handle JSON, interact with AWS services, work with the operating system, and manipulate dates and times.

2. **Environment Variable**:

   - The `BUCKET` environment variable is retrieved using `os.environ['BUCKET']`. This variable holds the name of the S3 bucket where the uncompressed logs will be stored.

3. **S3 Client**:

   - S3 client is created using `boto3.client("s3")` to interact with Amazon S3.

4. **Handler Function**:

   - The `handler` function is defined to process API Gateway requests. It takes `event` and `context` as parameters, which are provided by the API Gateway.

5. **Event Processing**:

   - The function extracts the day, month, and year to build the path for storing the log data.
   - retrieves the request body from the API Gateway request and parses it as JSON.
   - extracts the userId and log information from the request body and prepare to s3 upload.

6. **S3 Upload**:

   - The log data is uploaded to the specified S3 bucket using the `put_object` method, with the key structure based on the path, userId, and current time.

7. **Response**:
   - The function returns a 200 status code and a JSON response indicating the successful storage of the data.

This code essentially handles API Gateway requests, extracts and stores log data in an S3 bucket using AWS Lambda and the boto3 library.

### 4.`resources/compress.py`:

Certainly! This is a Python function that serves as an AWS Lambda handler for processing S3 events. Here's a breakdown of the code:

1. **Imports**:

   - The function imports necessary modules such as `json`, `boto3`, `os`, `datetime`, `urllib.parse`, `gzip`, and `io` to handle JSON, interact with AWS services, work with the operating system, manipulate dates and times, parse URLs, and handle gzip compression.

2. **Environment Variable**:

   - The function retrieves the `DEST` environment variable using `os.environ['DEST']`, likely holding the destination S3 bucket where the compressed data will be stored.

3. **S3 Client**:

   - An S3 client is created using `boto3.client("s3")` to interact with Amazon S3.

4. **Handler Function**:

   - The `handler` function is defined to process S3 events. It takes `event` and `context` as parameters, which are provided by the AWS Lambda service.

5. **Event Processing**:

   - The function extracts the day, month, and year to build the path for storing the compressed data.
   - Retrieves the bucket and object key from the S3 event, and decodes the object key.
   - Retrieves the object's content from the S3 bucket.

6. **Compression**:

   - The object's content is compressed using gzip, and the compressed data is stored in the destination S3 bucket.

7. **Response**:
   - The function returns a 200 status code and a JSON response indicating the successful storage of the data.

This code essentially handles S3 events triggered by object creation, compresses the object's content, and stores the compressed data in another S3 bucket.

## How-To-Deploy

Follow the steps below to deploy to AWS

- `python3 -m venv .venv` - prepare python vitual env
- `source .venv/bin/activate` - activate the venv
- `.venv\Scripts\activate.bat` - Only in case running on window
- `pip install -r requirements.txt` - Installing required dependencis
- `cdk bootstrap aws://${account}/${region}`- Setup aws account
- `cdk synth` - Generate cloud formation template
- `cdk deploy` - deploy to the aws account

exposing the function url still requried to be done manullay
