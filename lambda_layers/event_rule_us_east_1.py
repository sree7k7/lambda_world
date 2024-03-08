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
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["s3.amazonaws.com"],
                    "eventName": ["CreateBucket"],
                }
            ),
            rule_name="RuleToTriggerAnotherEvent",
        )
        # This rule sends a custom event to the EventBus in 'eu-central-1' region
        rule.add_target(targets.EventBus(
            event_bus=events.EventBus.from_event_bus_arn(
                self, 
                "EventBus", 
                event_bus_arn="arn:aws:events:eu-central-1:619831221558:event-bus/default"
            ),
            # input=events.RuleTargetInput.from_object({
            #     "source": ["custom.source"],
            #     "detail-type": ["Custom Event"],
            #     "detail": {}
            # })
        ))

# # when bucket is created in us-east-1, send a sns notification to email
# # create a sns topic
        topic = sns.Topic(self, "MyTopic",
            display_name="MyTopic",
            topic_name="MyTopic"
        )
        # create a subscription to the topic
        topic.add_subscription(sns.Subscription(
            endpoint="sree7k7@gmail.com",
            protocol=sns.SubscriptionProtocol.EMAIL,
            endpoint_auto_confirms=True
        ))