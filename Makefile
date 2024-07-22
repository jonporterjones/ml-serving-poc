make create_lambda_package:
	rm -rf ./resources/ml_serving_poc_package 
	mkdir ./resources/ml_serving_poc_package
	pip install --platform manylinux2014_x86_64 --only-binary=:all: --target ./resources/ml_serving_poc_package scikit-learn
	cd ./resources/ml_serving_poc_package && zip -r ../ml_serving_poc_package.zip ./*  -x '*/__pycache__/*' -x '*.pyc' '*.dist-info*'
	zip -j ./resources/ml_serving_poc_package.zip ./lambda/lambda_function.py
	