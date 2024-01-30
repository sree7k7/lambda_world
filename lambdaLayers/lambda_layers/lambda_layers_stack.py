from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_sns as sns,
)
from constructs import Construct
from aws_cdk import aws_lambda as _lambda
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns as sns
import aws_cdk.aws_s3 as s3


# get vpc stack
from lambda_layers.ec2 import VpcStack
from aws_cdk import CfnOutput
# from lambda_layers.stage import Stage

class LambdaLayersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create lambda function with layers

        # lambda_layer = _lambda.LayerVersion(
        #     self,
        #     "LambdaLayer",
        #     code=_lambda.Code.from_asset('python'),
        #     layer_version_name="AccountValidationLayer",
        #     compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
        #     description="A layer to include requests package",
        #     removal_policy=RemovalPolicy.DESTROY,
        # )

        # # create lambda function
        # lambda_acc = _lambda.Function(
        #     self,
        #     "LambdaAccValidation",
        #     function_name="LambdaAccValidation",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     handler="lambda_function.lambda_handler",
        #     code=_lambda.Code.from_asset('lambda'),
        #     layers=[lambda_layer]
        # )

##### -------------------------------------------------------------------------------------------------------------------------------------------------------------
       # # create lambda function ec2 instance change notification, ec2 will be stopped if the tag 'SPECIAL_EXECEPTION' is not present
        # this will work for future ec2 instance creation
        # lambda_ec2 = _lambda.Function(
        #     self,
        #     "LambdaEC2StateChange",
        #     function_name="LambdaEC2StageChange",
        #     runtime=_lambda.Runtime.PYTHON_3_12,
        #     code=_lambda.Code.from_asset('lambda_ec2_state_change'),
        #     handler="lambda_ec2_state_change.lambda_handler",
        #     role=iam.Role(
        #         self,
        #         "LambdaEC2StateChangeRole",
        #         assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        #         managed_policies=[
        #             iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
        #             iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
        #             iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
        #             iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEventBridgeFullAccess"),
        #             iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
        #             ],
        #         role_name="LambdaEC2StateChangeRole"
        #     )
        # )



        # ## cloudwatch event rule
        # ## create an cloudwatch event rule to trigger lambda function

        # rule = events.Rule(
        #     self, 
        #     "Rule",
        #     description="Rule to trigger lambda function",
        #     enabled=True,
        #     event_pattern=events.EventPattern(
        #         source=["aws.ec2"],
        #         detail_type=["EC2 Instance State-change Notification"],
        #         detail={
        #             "state": ["running"]
        #         }
        #     ),
        #     # targets=[events.LambdaFunction(lambda_ec2)],
        #     rule_name="RuleToTriggerLambdaFunctionWhenEC2StateChange",
        # )
        
        # # # add target to the rule
        # rule.add_target(targets.LambdaFunction(lambda_ec2))

        # # # create sns topic
        # sns_topic = sns.Topic(
        #     self,
        #     "SNSTopic",
        #     display_name="SNSTopic",
        #     topic_name="SNSTopic"
        # )

        # ## Add email destination to SNS topic
        # susbcription = sns.Subscription(
        #     self,
        #     "subscription",
        #     endpoint="sree7k7@gmail.com",
        #     protocol=sns.SubscriptionProtocol.EMAIL,
        #     topic=sns_topic,
        # )

        # ## output sns topic arn
        # output_1 = CfnOutput(
        #     self,
        #     "SNSTopicArn",
        #     value=sns_topic.topic_arn,
        #     description="SNSTopicArn"
        # )   

        # # # invoke lambda function
        # lambda_ec2.add_permission(
        #     "InvokePermission",
        #     principal=iam.ServicePrincipal("events.amazonaws.com"),
        #     action="lambda:InvokeFunction",
        #     source_arn="arn:aws:events:eu-central-1:619831221558:rule/RuleToTriggerLambdaFunctionWhenEC2StateChange",
        # )

#### -------------------------------------------------------------------------------------------------------------------------------------------------------------
        # # delete bucket if it's created in us-east-1 region
        # create lambda funtion to delete bucket if it's created in us-east-1 region

        s3_lambda = _lambda.Function(
            self,
            "LambdaS3",
            function_name="LambdaS3",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda'),
            handler="lambda_function.lambda_handler",
            timeout=Duration.seconds(300),
            role=iam.Role(
                self,
                "LambdaS3Role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEventBridgeFullAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
                    ],
                role_name="LambdaS3Role"
            )
        )

                ## cloudwatch event rule
        ## create an cloudwatch event rule to trigger lambda function
        rule = events.Rule(
            self, 
            "s3deleteRule",
            description="Rule to trigger lambda function",
            enabled=True,
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["s3.amazonaws.com"],
                    "eventName": ["CreateBucket"]
                }
            ),
            # targets=[events.LambdaFunction(lambda_ec2)],
            rule_name="RuleToTriggerLambdaFunctionWhenS3BucketCreated",
        )

        # # create sample event for AWS API Call via CloudTrail

                # # add target to the rule
        rule.add_target(targets.LambdaFunction(s3_lambda))

        # # invoke lambda function
        s3_lambda.add_permission(
            "InvokePermission",
            principal=iam.ServicePrincipal("events.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn="arn:aws:events:eu-central-1:619831221558:rule/RuleToTriggerLambdaFunctionWhenS3BucketCreated",
        )

        ## create bucket in us-east-1 region

        # s3_bucket = s3.Bucket(
        #     self,
        #     "S3Bucket",
        #     versioned=True,
        #     encryption=s3.BucketEncryption.S3_MANAGED,
        #     block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        #     removal_policy=RemovalPolicy.DESTROY,
        #     auto_delete_objects=True,
        # )