import boto3

ssm = boto3.client("ssm")

def get_param(name):
    return ssm.get_parameter(Name=name)["Parameter"]["Value"]

def assume_role(account_id, role_name):
    sts = boto3.client("sts")
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    creds = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="xacc-session"
    )["Credentials"]

    return boto3.client(
        "ec2",
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"]
    )

# Load values from SSM
accounts = get_param("/automation/accounts").split(",")
role_name = get_param("/automation/roleName")

for account_id in accounts:
    ec2 = assume_role(account_id, role_name)
    instances = ec2.describe_instances()

    print(f"--- Account {account_id} ---")
    for r in instances["Reservations"]:
        for i in r["Instances"]:
            print(i["InstanceId"], i["State"]["Name"])