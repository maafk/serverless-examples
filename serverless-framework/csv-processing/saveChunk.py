import boto3
import psycopg2
from smart_open import smart_open
import os

bucket = os.environ['bucket']
s3 = boto3.client('s3')

conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port='5432',
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    dbname='csv_process'
)

cur = conn.cursor()
db_table = 'artists'


def copy_from_s3_file_to_db(key):
    with smart_open(key, 'r') as fh:
        cur.copy_from(fh, db_table, sep=',')


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
