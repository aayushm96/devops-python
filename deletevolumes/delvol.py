import boto3
from datetime import datetime, timezone

ec2 = boto3.client("ec2")

def delete_unused_volumes(days_old=7, dry_run=True):
    """
    Delete EBS volumes that are in 'available' state (unattached)
    and older than given number of days.
    """

    response = ec2.describe_volumes(
        Filters=[
            {"Name": "status", "Values": ["available"]}  # unattached
        ]
    )

    now = datetime.now(timezone.utc)

    for volume in response["Volumes"]:
        vol_id = volume["VolumeId"]
        create_time = volume["CreateTime"]
        age_days = (now - create_time).days

        print(f"Found volume: {vol_id} | Age: {age_days} days")

        # Delete only after threshold age
        if age_days >= days_old:
            try:
                print(f"Deleting volume: {vol_id} (dry_run={dry_run})")
                ec2.delete_volume(VolumeId=vol_id, DryRun=dry_run)
                print(f"✓ Deleted: {vol_id}")
            except Exception as e:
                print(f"✗ Failed: {vol_id} | Error: {e}")
        else:
            print(f"Skipping (age < {days_old} days): {vol_id}")


if __name__ == "__main__":
    delete_unused_volumes(days_old=7, dry_run=False)   # Set dry_run=True for testing