import aws_cdk as core
import aws_cdk.assertions as assertions

from demo_app.demo_app_stack import DemoAppStack


# example tests. To run these tests, uncomment this file along with the example
# resource in jpj_demo_app/jpj_demo_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DemoAppStack(app, "demo-app")
    template = assertions.Template.from_stack(stack)

