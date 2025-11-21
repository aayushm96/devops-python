import boto3
from datetime import datetime, timezone

ec2 = boto3.client("ec2")

def delete_unused_volumes(days_old=7, dry_run=True):
    """
    Delete EBS volumes that are in 'available' state (unattached)
    and older than a given number of days.
    Pagination enabled.
    """

    paginator = ec2.get_paginator("describe_volumes")

    # Only find unattached (available) volumes
    page_iterator = paginator.paginate(
        Filters=[
            {"Name": "status", "Values": ["available"]}
        ]
    )

    now = datetime.now(timezone.utc)

    for page in page_iterator:
        for volume in page["Volumes"]:
            vol_id = volume["VolumeId"]
            create_time = volume["CreateTime"]
            age_days = (now - create_time).days

            print(f"Found volume: {vol_id} | Age: {age_days} days")

            # Skip if too new
            if age_days < days_old:
                print(f"Skipping (age < {days_old} days): {vol_id}")
                continue

            # Attempt deletion
            try:
                print(f"Deleting volume: {vol_id} (dry_run={dry_run})")
                ec2.delete_volume(VolumeId=vol_id, DryRun=dry_run)
                print(f"✓ Deleted: {vol_id}")
            except Exception as e:
                print(f"✗ Failed: {vol_id} | Error: {e}")


if __name__ == "__main__":
    delete_unused_volumes(days_old=7, dry_run=False)   # Set dry_run=True for safety testing