import boto3

# Default region required only for the describe_regions call
ec2_global = boto3.client("ec2", region_name="us-east-1")

regions = [r['RegionName'] for r in ec2_global.describe_regions()['Regions']]

for region in regions:
    ec2 = boto3.client('ec2', region_name=region)
    instances = ec2.describe_instances()

    print(f"--- {region} ---")
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(instance['InstanceId'], instance['State']['Name'])


