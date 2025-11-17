import boto3
import json

client = boto3.client("route53")

zones = client.list_hosted_zones()

output = []

for zone in zones["HostedZones"]:
    zone_id = zone["Id"]
    records = client.list_resource_record_sets(HostedZoneId=zone_id)

    output.append(
        {"HostedZone": zone["Name"], "Records": records["ResourceRecordSets"]}
    )

with open("route53_output.json", "w") as f:
    json.dump(output, f, indent=4)

print("Saved to route53_output.json")


