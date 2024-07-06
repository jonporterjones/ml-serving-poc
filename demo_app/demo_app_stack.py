import os

from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class DemoAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add the lambda
        # Lambda layer to provide sklearn within lambda limitations
        # This expects that layer to already exist.
        #my_layer = lambda_.LayerVersion.from_layer_version_arn(self,
        #    id="python-3-8-scikit-learn-0-23-1",
        #    layer_version_arn="arn:aws:lambda:us-east-1:446751924810:layer:python-3-8-scikit-learn-0-23-1:2")

        # I'll use an existing role for simplicity - it has s3 permissions.
        # In reality you would probably build role within this stack.
        # Lambda will auto-generate a role if none provided.
        # my_role = iam.Role.from_role_arn(self,
        #     id='role-ref',
        #     role_arn="arn:aws:iam::161089792558:role/service-role/lambda-01-role-8t9yyzoh")

        bucket_name_model = os.getenv(key="BUCKET_NAME_MODEL")
        file_name_model = os.getenv(key="FILE_NAME_MODEL")

        print(bucket_name_model)
        print(file_name_model)

        handler = lambda_.Function(self, "LambdaFunction",
                    runtime=lambda_.Runtime.PYTHON_3_9,
                    code=lambda_.Code.from_asset("./resources/ml_serving_package.zip"),
                    handler="lambda_function.lambda_handler",
                    memory_size=2048,
                    environment={
                            "S3_RESOURCE_ARN": f"arn:aws:s3:::{bucket_name_model}/{file_name_model}"
                    })

        #handler.add_layers(my_layer)

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
