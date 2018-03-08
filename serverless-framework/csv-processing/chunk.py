import os
import boto3
from smart_open import smart_open

bucket = os.environ['bucket']
s3 = boto3.client('s3')


def write_file_to_s3(filename, raw_key):
    s3.upload_file(
        Filename=filename,
        Bucket=bucket,
        Key=set_s3_file_name(filename, raw_key)
    )


def set_s3_file_name(filename, raw_key):
    split = filename.split('/')
    return "chunked/{}/{}".format(raw_key, split[-1])


def split(filehandler, raw_key, delimiter=',', row_limit=10000,
          output_name_template='output_%04d.csv', output_path='.',
          keep_headers=True):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:

        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));

    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(
        open(current_out_path, 'w'), delimiter=delimiter)

    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    has_been_written = False
    total_files_written = 0
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            prev_out_path = current_out_path
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(
                open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
            write_file_to_s3(prev_out_path, raw_key)
            total_files_written += 1
            has_been_written = True
            os.remove(prev_out_path)
        else:
            has_been_written = False
        current_out_writer.writerow(row)

    if not has_been_written:
        prev_out_path = current_out_path
        current_out_path = '/tmp/delete_this'
        current_out_writer = csv.writer(
            open(current_out_path, 'w'), delimiter=delimiter)
        write_file_to_s3(prev_out_path, raw_key)
        total_files_written += 1
        os.remove(prev_out_path)

    return total_files_written


def chunk_s3_file(s3_key):
    raw_key = s3_key.split('/')[-1]
    filehandler = smart_open(s3_key, 'r')
    results = split(
        filehandler=filehandler,
        keep_headers=False,
        output_path='/tmp',
        raw_key=raw_key
    )
    return {
        "total_files_written": results,
        "raw_file": raw_key    
    }


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


def chunk_raws(key_list):
    raw_files = []
    for key in key_list:
        raw_files.append(chunk_s3_file(key))


def handle_event(event):
    key_list = get_list_of_s3_keys_from_event(event)
    chunk_raws(key_list)


def main(event, context):
    handle_event(event)


if __name__ == '__main__':
    main()
