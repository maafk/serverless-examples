import boto3
import csv
import re
import os
from cryptography.fernet import Fernet
from smart_open import smart_open

bucket = os.environ['bucket']
s3 = boto3.client('s3')
out_dir = 'processed'

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# encryption
cipher_key = b'pDVbWWqjS9bwGRxTwJng2lyVMSkKe-hwtvvxDvQAmBs='
cipher = Fernet(cipher_key)


def process_file(s3_key):
    output_path = '/tmp'

    out_key = "/".join(s3_key.split('/')[-2:])
    outfile = os.path.join(output_path, out_key)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    o = open(outfile, 'w')
    out_writer = csv.writer(o)
    with smart_open(s3_key, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            valid = True
            processed_row = process_row(row)
            if valid:
                out_writer.writerow(processed_row)
    o.close()
    write_file_to_s3(outfile, s3_key)
    os.remove(outfile)


def write_file_to_s3(filename, raw_key):
    s3.upload_file(
        Filename=filename,
        Bucket=bucket,
        Key=set_s3_file_name(raw_key)
    )


def set_s3_file_name(raw_key):
    raw_split = raw_key.split('/')[4:]
    raw_split.insert(0, 'processed')
    return "/".join(raw_split)


def process_row(row):
    valid = True
    if not validate_email(row[2]):
        print("bad email {}".format(row[2]))
        valid = False
    row[4] = encrypt_field(row[4])

    if valid:
        return row
    else:
        print("Bad row: {}".format(row))


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


def encrypt_field(data):
    return cipher.encrypt(bytes(data, 'utf-8'))


def validate_email(email):
    return EMAIL_REGEX.match(email)


def main(event, context):
    keys = get_list_of_s3_keys_from_event(event)
    for key in keys:
        process_file(key)


if __name__ == '__main__':
    import json
    event = json.load(open('fixtures/new_file_chunked.json'))
    main(event, {})
