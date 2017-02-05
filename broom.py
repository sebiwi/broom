from __future__ import print_function

import json
import urllib
import boto3
import gzip
import io

print('Loading function')

# General services
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Values
SNS_TOPIC_ARN = 'arn:aws:sns:region:weird_number:topic_name'
CODES = ['LOL', 'GGG', 'BRB', 'YLO']


def decompress(data):
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as f:
        return f.read()


def report(instance, user, region):
    report = "User " + user + " created an instance on region " +  region + " without proper tagging. \n"
    report += "Instance id: " + instance['instanceId'] + "\n"
    report += "Image Id: " + instance['imageId'] + "\n"
    report += "Instance type: " + instance['instanceType'] + "\n"
    report += "This instance has been destroyed."
    return report


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        s3_object = s3.get_object(Bucket=bucket, Key=key)
        s3_object_content = s3_object['Body'].read()
        s3_object_unzipped_content = decompress(s3_object_content)
        json_object = json.loads(s3_object_unzipped_content)
        for record in json_object['Records']:
            if record['eventName'] == "RunInstances":
                user = record['userIdentity']['userName']
                region = record['awsRegion']
                ec2 = boto3.resource('ec2', region_name=region)
                for index, instance in enumerate(record['responseElements']['instancesSet']['items']):
                    instance_object = ec2.Instance(instance['instanceId'])
                    tags = {}
                    for tag in instance_object.tags:
                        tags[tag['Key']] = tag['Value']
                    if('Code' not in tags or tags['Code'] not in CODES):
                        instance_object.terminate()
                        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=report(instance, user, region))
    except Exception as e:
        print(e)
        raise e
