import boto3

# Global EC2 client for fetching all regions
ec2_global = boto3.client("ec2", region_name="us-east-1")

# Fetch region names
regions = [r["RegionName"] for r in ec2_global.describe_regions()["Regions"]]

for region in regions:
    print(f"--- {region} ---")
    
    ec2 = boto3.client("ec2", region_name=region)
    
    # Create paginator
    paginator = ec2.get_paginator("describe_instances")
    
    # Iterate through all pages
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                state = instance["State"]["Name"]
                print(instance_id, state)