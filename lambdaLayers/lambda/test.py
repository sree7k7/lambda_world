# import boto3
# s3 = boto3.client('s3')
# bucket_region = s3.get_bucket_location(Bucket='dasd619831221558')
# print("this is bucket region:-", bucket_region['LocationConstraint'])




import boto3
s3 = boto3.client('s3')
bucket_region = s3.get_bucket_location(Bucket='s3-inventory-report619831221558')['LocationConstraint']
bucket_region = bucket_region if bucket_region else 'us-east-1'
print("this is bucket region:-", bucket_region)