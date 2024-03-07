# #!/usr/bin/env python3
# import os
# import boto3

# import aws_cdk as cdk

# from lambda_layers.lambda_layers_stack import LambdaLayersStack
# from lambda_layers.ec2 import VpcStack
# from lambda_layers.event_rule_us_east_1 import EventRuleUsEast1Stack

# app = cdk.App()
# LambdaLayersStack(app, "LambdaLayersStack", 
#                     env=cdk.Environment(account='619831221558', region='eu-central-1'),
#     )
# # Get the list of all available regions
# ec2 = boto3.client('ec2')
# regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
# print(regions)
# # Create a stack for each region
# for region in regions:
#   EventRuleUsEast1Stack(app, "EventRuleUsEast1Stack", 
#                       env=cdk.Environment(account='619831221558', region=regions)
#                       )
# app.synth()

#!/usr/bin/env python3
import os
import boto3

import aws_cdk as cdk

from lambda_layers.lambda_layers_stack import LambdaLayersStack
from lambda_layers.ec2 import VpcStack
from lambda_layers.event_rule_us_east_1 import EventRuleUsEast1Stack

app = cdk.App()

# Get the list of all available regions
ec2 = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Create a stack for each region
for region in regions:
    LambdaLayersStack(app, f"LambdaLayersStack-{region}", 
                      env=cdk.Environment(account='619831221558', region=region))

app.synth()