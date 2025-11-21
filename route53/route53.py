import boto3
from openpyxl import Workbook

# Create Route53 client with clear name
r53 = boto3.client("route53")

# ------------------------
# Create Excel Workbook
# ------------------------
wb = Workbook()
ws = wb.active
ws.title = "Route53 Records"

# Excel header row
ws.append(["Hosted Zone", "Record Name", "Record Type", "TTL", "Record Value"])

# ------------------------
# Fetch Hosted Zones
# ------------------------
zones = r53.list_hosted_zones()["HostedZones"]

# ------------------------
# Loop zones & paginate record sets
# ------------------------
for zone in zones:
    zone_id = zone["Id"]
    zone_name = zone["Name"]

    paginator = r53.get_paginator("list_resource_record_sets")

    # Iterate over ALL pages
    for page in paginator.paginate(HostedZoneId=zone_id):
        records = page["ResourceRecordSets"]

        for record in records:
            name = record.get("Name", "")
            rtype = record.get("Type", "")
            ttl = record.get("TTL", "")

            # A/TXT/MX records (multiple values)
            if "ResourceRecords" in record:
                for rr in record["ResourceRecords"]:
                    ws.append([zone_name, name, rtype, ttl, rr["Value"]])

            # Alias targets (ALB, CloudFront, etc.)
            elif "AliasTarget" in record:
                alias_dns = record["AliasTarget"].get("DNSName", "")
                ws.append([zone_name, name, rtype, ttl, alias_dns])

            # Records with no values (rare)
            else:
                ws.append([zone_name, name, rtype, ttl, ""])

# Save Excel File
excel_file = "route53_output.xlsx"
wb.save(excel_file)

print(f"Saved all Route53 records to {excel_file} using Route53 client (r53).")