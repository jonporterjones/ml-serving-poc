import os

from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class DemoAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name_model = os.getenv(key="BUCKET_NAME_MODEL")
        file_name_model = os.getenv(key="FILE_NAME_MODEL")

        handler = lambda_.Function(self, "LambdaFunction",
                    runtime=lambda_.Runtime.PYTHON_3_11,
                    code=lambda_.Code.from_asset("./resources/ml_serving_poc_package.zip"),
                    handler="lambda_function.lambda_handler",
                    memory_size=2048,
                    environment={
                        "BUCKET_NAME_MODEL": os.getenv(key="BUCKET_NAME_MODEL"),
                        "FILE_NAME_MODEL": os.getenv(key="FILE_NAME_MODEL")
                    })

        # Add the API Gateway
        api = apigateway.RestApi(self, "ApiGateway",
            rest_api_name="API Gateway from CDK",
            description="API Gateway handles request for predictive service.",
            endpoint_types=[apigateway.EndpointType.REGIONAL])

        # Define integration response
        integration_response = apigateway.IntegrationResponse(status_code="200")

        # This part tooks some time to figure out.
        method_response = apigateway.MethodResponse(
            status_code="200", 
            response_models={"application/json": apigateway.Model.EMPTY_MODEL})

        # There are a number of integrations with API Gateway.
        # This one uses lambda
        api_lambda_integration = apigateway.LambdaIntegration(
            handler,
            proxy=False,
            integration_responses=[integration_response])

        # Post with a body is the only method supported.
        api.root.add_method("POST", 
        api_lambda_integration, 
        method_responses=[method_response])
