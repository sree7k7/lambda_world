import aws_cdk as cdk
from constructs import Construct

from lambda_layers.ec2  import VpcStack
from lambda_layers.lambda_layers_stack import LambdaLayersStack
# from cdk_pipeline_simulated_corporate_network.ec2 import EC2



class Stage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, config: object, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # network = Network(
        #     self,
        #     'Network',
        #     config = config
        # )
        ec2 = EC2(
            self,
            "DnacServer",
            # vpc = network.vpc,

            # config = config,

            # sg_group = network.sg_group         
        )    


