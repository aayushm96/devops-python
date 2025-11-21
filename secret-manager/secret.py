import boto3
import json

def get_secret(secret_name, region="ap-south-1"):
    client = boto3.client("secretsmanager", region_name=region)

    response = client.get_secret_value(SecretId=secret_name)

    print(response)

    if "SecretString" in response:
        return json.loads(response["SecretString"])   # returns dict
    else:
        return response["SecretBinary"]               # rarely used
