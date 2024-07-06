make create_lambda_package:
	mkdir ./resources/ml_serving_poc_package
	pip install --target ./resources/ml_serving_poc_package boto3 constructs scikit-learn==1.5.0
	zip -r ./resources/ml_serving_poc_package.zip ./resources/ml_serving_poc_package -x '*/__pycache__/*' -x '*.pyc' '*.dist-info*'
	zip -j ./resources/ml_serving_poc_package.zip ./lambda/lambda_function.py