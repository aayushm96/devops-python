import csv
import requests
from openpyxl import Workbook

csv_file = './data.csv'
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
ws.append(["URL", "Response"])

# Step 3: Curl each URL and collect only the response
for url in urls:
    try:
        response = requests.get("https://{url}", timeout=5)
        body = response.text
    except Exception as e:
        body = f"ERROR: {str(e)}"
    
    # Write row into Excel
    ws.append([url, body])

# Step 4: Save Excel file
wb.save("responses.xlsx")

print("Saved all responses to responses.xlsx")