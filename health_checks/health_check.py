import csv
import sys
import requests
from openpyxl import Workbook

# CSV file from command line
csv_file = sys.argv[1]

urls = []

# Step 1: Read URLs from CSV
with open(csv_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        urls.append(row[0].strip())

# Step 2: Create Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Responses"

# Create headers
ws.append(["URL", "Response", "Status Code"])

# Step 3: Curl each URL and collect response
for url in urls:
    try:
        url = f"https://{url}"
        response = requests.get(url, timeout=5)
        body = response.text
        status_code = response.status_code
    except Exception as e:
        body = f"Error: {str(e)}"
        status_code = "N/A"

    # Write row into Excel
    ws.append([url, body, status_code])

# Step 4: Save Excel file
wb.save("responses.xlsx")
print("Saved all responses to responses.xlsx")