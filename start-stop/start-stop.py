import boto3

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