import json
import os
import pickle

import boto3

bucket_name_model = os.getenv("BUCKET_NAME_MODEL")
file_name_model = os.getenv("FILE_NAME_MODEL")

def lambda_handler(event, context):
    
    # Download model from s3
    # Lambda is a read-only file system with the exception of /tmp
    # You can define the size of /tmp as well
    # This sort of operation can also be done in memory only, which would be preferrable.
    s3 = boto3.resource('s3')
    s3.Object(bucket_name=bucket_name_model, key=file_name_model).download_file('/tmp/model.pkl')

    # Unpickle model
    model = pickle.load(open('/tmp/model.pkl', mode='r+b'))

    # Make a prediction
    # event parameter is method POST body as-is, no need to further manipulate it.
    prediction = model.predict(event)

    # 0,1,2 (Setosa, Versicolour, and Virginica)
    output_classes = {
        0: "Setosa",
        1: "Versicolour",
        2: "Virginica"
    }

    # format prediction to actual labels
    prediction_output = [output_classes[pred] for pred in prediction]

    # return http response.
    return {
        'statusCode': 200,
        'body': json.dumps(prediction_output)
    }