import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_layers.lambda_layers_stack import LambdaLayersStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_layers/lambda_layers_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaLayersStack(app, "lambda-layers")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
