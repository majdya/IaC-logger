import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_s3_notifications,
                     aws_lambda as lambda_)

class LogUploadService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        bucket = s3.Bucket(self, "UploadHandler")
        bucket2 = s3.Bucket(self, "CompressHandler")

        uploadHandler = lambda_.Function(self, "bucket",
                    runtime=lambda_.Runtime.PYTHON_3_11,
                    code=lambda_.Code.from_asset("resources"),
                    handler="upload.handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )

        bucket.grant_read_write(uploadHandler)

        api = apigateway.RestApi(self, "upload-api",
                  rest_api_name="Upload Service",
                  description="This service serves uploaded logs.")

        upload_integration = apigateway.LambdaIntegration(uploadHandler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", upload_integration)   # POST /

        compressHandler = lambda_.Function(self, "bucket2",
                    runtime=lambda_.Runtime.PYTHON_3_11,
                    code=lambda_.Code.from_asset("resources"),
                    handler="compress.handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name,
                    DEST=bucket2.bucket_name)
                    )

        bucket.grant_read(compressHandler)
        bucket2.grant_read_write(compressHandler)

        notification = aws_s3_notifications.LambdaDestination(compressHandler)

        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)
        # widget = api.root.add_resource("/compress")
        # widget_integration = apigateway.LambdaIntegration(handler)
        # widget.add_method("POST", widget_integration);   # POST /compress

        # widget = api.root.add_resource("{id}")
        # widget_integration = apigateway.LambdaIntegration(handler)
        # widget.add_method("POST", widget_integration);   # POST /{id}
        # widget.add_method("GET", widget_integration);    # GET /{id}
        # widget.add_method("DELETE", widget_integration); # DELETE /{id}