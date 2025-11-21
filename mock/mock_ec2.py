# from moto import mock_aws
# import boto3

# @mock_aws
# def test_ec2():
#     ec2 = boto3.client("ec2", region_name="us-east-1")
#     ec2.run_instances(ImageId='ami-123456', MinCount=1, MaxCount=1)
#     print(ec2.describe_instances())

from moto import mock_aws
import boto3

@mock_aws
def test_s3():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="demo-bucket")
    print(s3.list_buckets())

test_s3()

def smart_action(instance_id, region="ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)

    status = ec2.describe_instance_status(
        InstanceIds=[instance_id],
        IncludeAllInstances=True
    )['InstanceStatuses'][0]['InstanceState']['Name']

    if status == "stopped":
        print("Instance is stopped → starting...")
        ec2.start_instances(InstanceIds=[instance_id])

    elif status == "running":
        print("Instance is running → stopping...")
        ec2.stop_instances(InstanceIds=[instance_id])

    else:
        print(f"Instance is in state: {status}, no action taken")

smart_action("i-0123456789abcdef0")