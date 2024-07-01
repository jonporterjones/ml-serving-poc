# ML Serving POC

Serve a simple ml model with API Gateway and Lambda

## Starting

This POC will use boto3, aws cdk, and web service constructs for deployment.
It will use sklearn for model building a model and the artifact.
Create a virtual environment and install with requirements.txt.

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

### Deploy Resources:

demo_app/demo_app_stack contains the actual CloudFormation stack.
It defines the resources that will be deployed to AWS.
They are:
a lambda layer pre-built for sklearn
an iam role with proper permissions
The lambda handler function definition
API Gateway integrated with Lambda to provide a callable endpoint

The trained model will be expected to be found in s3.