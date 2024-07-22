# ML Serving POC

Serve a simple ml model with API Gateway and Lambda

## Starting

This POC will use boto3, aws cdk, and web service constructs for deployment.
It will use sklearn for model building a model and the artifact.
Create a virtual environment and install with requirements.txt.

This code assumes that aws cdk is installed on the workstation
and that the account being deployed to is bootstrapped for cdk deployments.

## Model

The model itself is not very important.
Use the IRIS dataset from sklearn and train it in the model folder.
This POC assumes a trained model exists, execute model/build_model.py
to get a model file resources/model.pkl

Copy this artifact into an s3 bucket.
Use the aws cmd line utility:
"aws s3 cp resources/model.pkl s3://build-artifacts-766551654251/ml-serving-poc-model.pkl"

## Deploy

The deployment uses CDK to generate and deploy a CloudFormation stack

Generate to view stack locally: cdk synth --app "python app.py"
Deploy to aws: cdk deploy --app "python app.py" --profile default

This document won't explain AWS authentication and IAM permissions in great detail,
the profile specified in the deploy statement will identify the account, region, and permissions used for the deploy operation.

### Environment Variables

The lambda function code uses 2 environment variables
BUCKET_NAME_MODEL
FILE_NAME_MODEL
These need to be set on the workstation doing the deployment and they will be copied
into the CFN stack and used in the execution to download the model.

### Deploy Resources:

demo_app/demo_app_stack contains the actual CloudFormation stack.
It defines the resources that will be deployed to AWS.
They are:
a lambda layer pre-built for sklearn
an iam role with proper permissions
The lambda handler function definition
API Gateway integrated with Lambda to provide a callable endpoint

The trained model will be expected to be found in s3.

### Lambda Deployment package

Lambda needs a deployment package containing the code to be executed and any dependencies.
This poc uses the simplest method, a single zip file, but this can also be done with
a lambda layer
or a container image

a Makefile target create_lambda_package exists to create the deployment package.

## Gotcha's

Make certain the IAM role assigned to the lambda function can download from S3.

## Testing

Test through the AWS Console in API Gateway or using Postman 
Sample request body:
[[3.1, 2.7, 0.1, 3.0],[7.2, 3.6, 4.1, 5.0]]