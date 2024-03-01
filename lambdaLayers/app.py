#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lambda_layers.lambda_layers_stack import LambdaLayersStack
from lambda_layers.ec2 import VpcStack
from lambda_layers.event_rule_us_east_1 import EventRuleUsEast1Stack

app = cdk.App()
LambdaLayersStack(app, "LambdaLayersStack", 
                    env=cdk.Environment(account='619831221558', region='eu-central-1')
                  # output value of lambdaname
                  
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='619831221558', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
# VpcStack(app, "VpcStack",
# )
# EventRuleUsEast1Stack(app, "EventRuleUsEast1Stack", 
                    #   env=cdk.Environment(account='619831221558', region='us-east-1')
                    #   )
app.synth()