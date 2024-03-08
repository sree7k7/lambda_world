from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_sns as sns,
    aws_logs as logs,

)
from constructs import Construct
from aws_cdk import aws_lambda as _lambda
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns as sns
import aws_cdk.aws_s3 as s3

from aws_cdk import CfnOutput
from aws_cdk import aws_cloudtrail
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
                # assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),

                assumed_by=iam.CompositePrincipal(
                    iam.ServicePrincipal("lambda.amazonaws.com"),
                    iam.ServicePrincipal("events.amazonaws.com"),
                ),
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
                    ],
                role_name="LambdaS3Role",
            )
        )

        # # create a couldtrail trail to capture s3 bucket creation event
        s3_trail = s3.Bucket(
            self,
            "s3trailforbucketcreation",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            event_bridge_enabled=True,
        )

        # # create cloudtrail trail

        log_group = logs.LogGroup(
            self,
            "loggroup",
            log_group_name="loggroup-s3trail",
            removal_policy=RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.ONE_DAY,
        )

        # # create cloudtrail trail
        cloudtrail_trail = aws_cloudtrail.Trail(
            self,
            "cloudtrailtrailforbucketcreation",
            bucket=s3_trail,
            is_multi_region_trail=True,
            include_global_service_events=True,
            send_to_cloud_watch_logs=True,
            enable_file_validation=True,
            trail_name="CustomCloudTrail",
            # management_events=aws_cloudtrail.ReadWriteType.ALL,
            cloud_watch_logs_retention=logs.RetentionDays.ONE_DAY,
            cloud_watch_log_group=log_group,
            # Specify data events
        )
        # Adds an event selector to the bucket foo
        cloudtrail_trail.add_s3_event_selector(
            include_management_events=True,
            s3_selector=[aws_cloudtrail.S3EventSelector(bucket=s3_trail, object_prefix="")],
            exclude_management_event_sources=[
                aws_cloudtrail.ManagementEventSources.KMS,
                aws_cloudtrail.ManagementEventSources.RDS_DATA_API,
                ],
            read_write_type=aws_cloudtrail.ReadWriteType.ALL,
        )

        # # cloudwatch event rule
        # # create an cloudwatch event rule. Trigger the rule when s3 bucket is created in us-east-1 region. And trigger lambda function
        # # matach the event pattern with the event pattern in the cloudtrail trail created above

        rule = events.Rule(
            self, 
            "s3deleteRule",
            description="Rule to trigger lambda fn",
            # event_bus=bus,
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["s3.amazonaws.com"],
                    "eventName": ["CreateBucket"],
                }
            ),
            rule_name="RuleToTriggerLambdaFunctionWhenS3BucketCreatedInWrongRegion",
        )
        rule.add_target(targets.LambdaFunction(s3_lambda))
        

        # rule.add_target(targets.EventBus(bus))

        # # invoke lambda function
        s3_lambda.add_permission(
            "InvokePermission",
            principal=iam.ServicePrincipal("events.amazonaws.com"),
            action="lambda:InvokeFunction",
            # source_arn="arn:aws:events:eu-central-1:619831221558:rule/RuleToTriggerLambdaFunctionWhenS3BucketCreatedInWrongRegion",
            source_arn="arn:aws:events:eu-central-1:619831221558:event-bus/default",
        )

        # # output lambda function name

        lambdaname = CfnOutput(
            self,
            "LambdfnName",
            value=s3_lambda.function_name,
            description="LambdaS3"
        )

    # # # create an s3 bucket in us-east-1 region
    #     s3_bucket = s3.Bucket(
    #         self,
    #         "s3bucket",
    #         removal_policy=RemovalPolicy.DESTROY,
    #         auto_delete_objects=True,
    #         versioned=True,
    #         encryption=s3.BucketEncryption.S3_MANAGED,
    #         block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
    #         event_bridge_enabled=True,
    #         bucket_name="sran619831221558-1",
    #     )