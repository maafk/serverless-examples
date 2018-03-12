import boto3
import psycopg2
from smart_open import smart_open
import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bucket = os.environ['bucket']
s3 = boto3.client('s3')

try:
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port='5432',
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        dbname='csv_process',
        connect_timeout=5
    )
except:
    logger.error(
        "ERROR: Unexpected error: Could not connect to Postgres instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")

cur = conn.cursor()
db_table = 'artists'


def copy_from_s3_file_to_db(key):
    f = smart_open(key, 'r')
    cur.copy_from(f, db_table, sep=',')
    f.close()


def get_list_of_s3_keys_from_event(event):
    key_list = []
    for record in event['Records']:
        key_list.append(
            "s3://{}/{}".format(
                record['s3']['bucket']['name'],
                record['s3']['object']['key']
            )
        )
    return key_list


def main(event, context):
    keys = get_list_of_s3_keys_from_event(event)
    for key in keys:
        copy_from_s3_file_to_db(key)
    conn.commit()
    cur.close()
    conn.close()
