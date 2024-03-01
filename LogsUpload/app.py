#!/usr/bin/env python3
import aws_cdk as cdk

from log_upload_service.log_upload_service_stack import LogUploadServiceStack

app = cdk.App()
LogUploadServiceStack(app, "LogUploadServiceStack" )

app.synth()
