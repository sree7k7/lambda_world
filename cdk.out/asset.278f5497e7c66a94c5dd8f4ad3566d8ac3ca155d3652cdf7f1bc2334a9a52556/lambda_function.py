import json
import boto3
import os

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement
    # # if bucket created in us-east-1, then delete bucket
    
    bt_region = event['detail']['awsRegion']
    print(bt_region)
    # bucketName = event['detail']['requestParameters']['bucketName'] 
    # print(bucketName)


    # list aws s3 buckets

    s3_list_response = s3.list_buckets()

    print(s3_list_response)
    print('printed s3 list response-------------------')

    bucketList = s3_list_response['Buckets']
    # print bucket list
    print(bucketList)


    for bucket in bucketList:
        bucket_region = s3.get_bucket_location(
            Bucket=bucket['Name'],
        )
        print(bucket_region)
        print('printed bucket region-------------------')
        print(bucket_region['LocationConstraint'])

        # # don't delete any bucket name starting with 'cdk-'
        if bucket['Name'].startswith('cdk-'):
            print('not deleting bucket starting with cdk-', bucket['Name'])
            continue
        
        # if bucket region not equals to eu-central-1, then delete bucket
        if  bucket_region['LocationConstraint'] != 'eu-central-1':
        # if  bt_region != 'eu-central-1':

            # print ("Event bucket region", bt_region)
            # check if bucket has objects
            print('Working ON Bucket', bucket['Name'], "in region", bucket_region['LocationConstraint'])
            # list all objects in the bucket

            object_response = s3.list_objects_v2(Bucket=bucket['Name'])
            print("printing bucket response", object_response, "from bucket", bucket['Name'])
            if 'Contents' in object_response:
                print('bucket has objects, bucket name', bucket['Name'])
                # delete all objects in the bucket
                for object in object_response['Contents']:
                    print('deleting object', object['Key'], "from bucket", bucket['Name'])
                    s3.delete_object(Bucket=bucket['Name'], Key=object['Key'])
                    print('deleted object', object['Key'], "from bucket", bucket['Name'])

                    # delete bucket when the objects are deleted
                    print('deleting bucket', bucket['Name'])
                    s3.delete_bucket(
                        Bucket=bucket['Name'],
                    )
                    print('deleted bucket for empty objects', bucket['Name'])
            else:
                print('bucket has no objects, bucket name', bucket['Name'])
            # delete bucket
                print('bucket created in region', bucket_region['LocationConstraint'], "bucket name", bucket['Name'])
                print('deleting bucket in another region', bucket['Name'], "bucket region", bucket_region['LocationConstraint'])
                s3.delete_bucket(
                        Bucket=bucket['Name'],
                    )
                print('deleted bucket in another region', bucket['Name'], "bucket region", bucket_region['LocationConstraint'])

        else:
            print('not deleting bucket in eu-central-1', bucket['Name'])

###### -------------------------------------------------------------------------------------------------------------------------------------------------------------

# # event based lambda function

# def lambda_handler(event, context):
#     # TODO implement
#     # bucket_region_event = event['awsRegion']
#     # print(bucket_region_event)

#     # list aws s3 buckets
#     s3_list_buckets = s3.list_buckets()
#     for bucket in s3_list_buckets['Buckets']:
#         print("Bucket name:", bucket['Name'])

#         # get bucket region
#         bucket_region = s3.get_bucket_location(
#             Bucket=bucket['Name'],
#         )

#         # delete bucket if bucket region not equals to eu-central-1
#         if  bucket_region['LocationConstraint'] != 'eu-central-1':
#             print('deleting bucket in another region', bucket['Name'])
#             s3.delete_bucket(
#                 Bucket=bucket['Name'],
#             )
#             print('deleted bucket in another region', bucket['Name'])
#         else:
#             print('not deleting bucket in eu-central-1', bucket['Name'])



            # print(bucket_region)
        # for item in bucket['Name']:
        #     print(item)
            # # get bucket region




    ## get bucket region
        
    # print("The value of is:", bucket['Name'])


    # print('printed bucket list-------------------')

    # bucket_region = s3.get_bucket_location(
    #     Bucket=bucket['Name'],
    # )
    # print(bucket_region)

    # for bucket in s3_list_response['Buckets']:
    #     print(bucket['Name'])




        # print bucket region

        # print('printed bucket region-------------------')
        # print(bucket[''])
    # if bucket == 'us-east-1':
    #         print('bucket created in us-east-1')
    #         bucket_name = event['detail']['requestParameters']['bucketName']
    #         print(bucket_name)

    #         response = s3.delete_bucket(
    #             Bucket=bucket_name
    #         )
    #         print(response)
    #         print('deleted bucket in us-east-1')
    #         return {
    #             'statusCode': 200,
    #             'body': json.dumps('bucket created in us-east-1')
    #         }
    # else:
    #         print('bucket created in another region')
    #         return {
    #             'statusCode': 200,
    #             'body': json.dumps('bucket created in another region')
    #         }



# {
#   "version": "0",
#   "id": "bfaeac7f-a57f-ddc8-2058-2e2aa99fd13d",
#   "detail-type": "AWS API Call via CloudTrail",
#   "source": "aws.s3",
#   "account": "123456789012",
#   "time": "2018-12-18T00:23:14Z",
#   "region": "us-east-1",
#   "resources": [],
#   "detail": {
#     "eventVersion": "1.05",
#     "userIdentity": {
#       "type": "Root",
#       "principalId": "123456789012",
#       "arn": "arn:aws:iam::123456789012:root",
#       "accountId": "123456789012",
#       "accessKeyId": "ASIA5DVXEBQOEA7B2ISB",
#       "sessionContext": {
#         "attributes": {
#           "creationDate": "2018-12-17T23:55:39Z",
#           "mfaAuthenticated": "false"
#         }
#       }
#     },
#     "eventTime": "2018-12-18T00:23:14Z",
#     "eventSource": "s3.amazonaws.com",
#     "eventName": "GetObjectLockLegalHold",
#     "awsRegion": "us-east-1",
#     "sourceIPAddress": "0.0.0.0",
#     "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.467 Linux/4.9.124-0.1.ac.198.73.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.192-b12 java/1.8.0_192]",
#     "requestParameters": {
#       "legal-hold": "",
#       "bucketName": "wwww619831221558",
#       "key": "any_aws_health"
#     },
#     "responseElements": null,
#     "additionalEventData": {
#       "objectRetentionInfo": {
#         "legalHoldInfo": {
#           "isUnderLegalHold": true,
#           "lastModifiedTime": 1545092274892
#         }
#       },
#       "x-amz-id-2": "pAiOLlb/y6zpfhkP3jjWeV3mYzzEhU+QxuINK7G0F6hC/5UiulPGp7AAIUOx0I8UGp+8FrfyIng="
#     },
#     "requestID": "76468D5F44AF2A7E",
#     "eventID": "a5c45bc2-8d9f-4c96-b273-50460a03aecc",
#     "readOnly": true,
#     "resources": [{
#       "type": "AWS::S3::Object",
#       "ARN": "arn:aws:s3:::bucket-with-lock/any_aws_health"
#     }, {
#       "accountId": "123456789012",
#       "type": "AWS::S3::Bucket",
#       "ARN": "arn:aws:s3:::bucket-with-lock"
#     }],
#     "eventType": "AwsApiCall",
#     "recipientAccountId": "123456789012",
#     "vpcEndpointId": "vpce-38d25651"
#   }
# }





# #-------------------------------------------------------------------------------------------------------------------------------------------------------------
            


# {
#    "detail":{
#       "requestParameters":{
#          "bucketName":"wwww619831221558"
#       }
#    }
# }

