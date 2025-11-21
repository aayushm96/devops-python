import boto3
import json
from openpyxl import Workbook

client = boto3.client("route53")

zones = client.list_hosted_zones()

output = []

# Collect all data
for zone in zones["HostedZones"]:
    zone_id = zone["Id"]
    records = client.list_resource_record_sets(HostedZoneId=zone_id)

    output.append({
        "HostedZone": zone["Name"],
        "Records": records["ResourceRecordSets"]
    })

# ---------------------------
# Write to Excel (.xlsx)
# ---------------------------

wb = Workbook()
ws = wb.active
ws.title = "Route53 Records"

# Header row
ws.append(["Hosted Zone", "Record Name", "Record Type", "TTL", "Record Value"])

for zone_data in output:
    hosted_zone = zone_data["HostedZone"]
    
    for record in zone_data["Records"]:
        name = record.get("Name", "")
        rtype = record.get("Type", "")
        ttl = record.get("TTL", "")

        # Records can have multiple values
        values = record.get("ResourceRecords", [])
        if values:
            for v in values:
                ws.append([hosted_zone, name, rtype, ttl, v["Value"]])
        else:
            # For ALIAS records, no ResourceRecords
            alias = record.get("AliasTarget", {})
            if alias:
                ws.append([hosted_zone, name, rtype, ttl, alias.get("DNSName", "")])
            else:
                ws.append([hosted_zone, name, rtype, ttl, ""])

# Save Excel file
excel_file = "route53_output.xlsx"
wb.save(excel_file)

print(f"Saved to {excel_file}")