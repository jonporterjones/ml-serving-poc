import json
import os
import pickle

import boto3

s3_resource_arn = os.getenv("S3_MODEL_ARN")

def lambda_handler(event, context):
    
    # Download model from s3
    # Lambda is a read-only file system with the exception of /tmp
    # You can define the size of /tmp as well
    # This sort of operation can also be done in memory only, which would be preferrable.
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('jpj-aws-cdk')
    obj = bucket.Object('model.pkl')
    s3.Object('jpj-aws-cdk', 'model.pkl').download_file('/tmp/model.pkl')

    # Unpickle modelm        
    model = pickle.load(open('/tmp/model.pkl', mode='r+b'))

    # Make a prediction
    # event parameter is method POST body as-is, no need to further manipulate it.
    prediction = model.predict(event)

    # return http response.
    return {
        'statusCode': 200,
        'body': json.dumps(prediction.tolist())
    }