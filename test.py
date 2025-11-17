import boto3

session = boto3.Session(profile_name="aayush")
ec2 = session.client("ec2")

instances = ec2.describe_instances()
print(instances)