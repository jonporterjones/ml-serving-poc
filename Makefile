make create_lambda_package:
	mkdir ./resources/ml_serving_poc_package
	pip install --platform manylinux2014_x86_64 --only-binary=:all: --target ./resources/ml_serving_poc_package scikit-learn==1.5.1
	cd ./resources/ml_serving_poc_package && zip -r ../ml_serving_poc_package.zip ./*  -x '*/__pycache__/*' -x '*.pyc' '*.dist-info*'
	zip -j ./resources/ml_serving_poc_package.zip ./lambda/lambda_function.py
	