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


class EventRuleUsEast1Stack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create a cloudwatch event rule to trigger lambda function in eu-central-1 region

        rule = events.Rule(self, 
            "s3deleteRule",
            description="Rule to trigger lambda function",
            enabled=True,
            event_bus=None,
            cross_stack_scope=None,
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["s3.amazonaws.com"],
                    "eventName": ["CreateBucket"],
                    # get event if the bucket is created in us-east-1 region
                    # "requestParameters": {
                    #     "bucketRegion": ["us-east-1"]
                    # },
                }
            ),
            rule_name="RuleToTriggerLambdaFunctionWhenS3BucketCreatedInWrongRegion",
        )

    # ## create a eventbrige bus to trigger event rule in eu-central-1 region
    #     bus = events.EventBus(self, "bus",
    #                           event_bus_name="bus-cdk-us-east-1"
    #                           )
    #     rule.add_target(targets.EventBus(bus))


                               