from constructs import Construct

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)

from . import log_upload_service

class LogUploadServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        log_upload_service.LogUploadService(self, "LogUpload")
