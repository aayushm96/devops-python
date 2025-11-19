import sys
import csv
import boto3
import logging

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename="tagger.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

logger = logging.getLogger(__name__)
# ------------------------------------------------

ec2 = boto3.client('ec2')

csv_file = sys.argv[1]

tags = {
    "system-manager": "b2c-start-stop",
    "scheduler": "yes",
}

with open(csv_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        resource_id = row[0].strip()
        if not resource_id:
            continue

        logger.info(f"Tagging resource: {resource_id}")

        tag_list = [{"Key": key, "Value": value} for key, value in tags.items()]

        for key, value in tags.items():
            logger.info(f" - Adding tag {key}: {value}")

        try:
            ec2.create_tags(
                Resources=[resource_id],
                Tags=tag_list
            )
            logger.info(f"Successfully tagged {resource_id}\n")

        except Exception as e:
            logger.error(f"Failed to tag {resource_id}: {e}\n")