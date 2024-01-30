# create a vpc, private subnet, route table, route table association, security group, ec2 instance, and an s3 bucket in cdk v2
from aws_cdk import (
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
    Stack,
    CfnOutput,
    Tags,
    aws_sns as sns,
)

from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create vpc
        vpc = ec2.Vpc(
            self,
            "VPC",
            cidr="10.0.1.0/16",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )

        # create security group
        sg = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow ssh access to ec2 instances",
            security_group_name="Allow_SSH"
        )

        # add ingress rule to security group
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "allow ssh access from the world"
        )

        # create ec2 instance
        ec2_instance = ec2.Instance(
            self,
            "EC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            security_group=sg,
            propagate_tags_to_volume_on_creation=True,
            # key_name="cdk"s
            # tags={
            #     "SPECIAL_EXECEPTION": "Server"
            # }
        )

        # add tags to ec2 instance
        Tags.of(ec2_instance).add("SPECIAL_EXECEPTION", "server")

        # create s3 bucket
        s3_bucket = s3.Bucket(
            self,
            "S3Bucket",
            bucket_name="cdk-s3-bucket-1234567890",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY
        )


        # create ssm parameter