import json
import boto3

client = boto3.client('ec2')
snsclient = boto3.client('sns')

def lambda_handler(event, context):
    # TODO implement
    ec2_instance=event['detail']['instance-id']
    print (ec2_instance)
    tag_response = client.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [ec2_instance]
            },
        ]
    )

    print (tag_response)
    print('printed tag-response-------------------')

    alltags=tag_response['Tags']
    # print (alltags)
    # print('printed alltags-------------------')

# stop the instance if the tag 'SPECIAL_EXECEPTION' is not present
    for tag in alltags:
        if tag['Key'] == 'SPECIAL_EXECEPTION':
            print('SPECIAL_EXECEPTION tag is present')
            return {
                'statusCode': 200,
                'body': json.dumps('SPECIAL_EXECEPTION tag is present')
            }
    else:
        print('SPECIAL_EXECEPTION tag is not present')
        print('stopping the instance')
        response = client.stop_instances(
            InstanceIds=[
                ec2_instance,
            ]
        )
        print(response)
        print('printed response-------------------')

 # SNS topic alert if the ec2 instance is stopped
    # topicarn='arn:aws:sns:eu-central-1:619831221558:SNSTopic'
    # sns = snsclient.publish(
    #     TopicArn=topicarn,
    #     Message='error message',
    #     Subject='Ec2 Violation Company policy!! Manager will be notified',
    # )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
