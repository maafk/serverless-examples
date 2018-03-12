# Processing large CSV files using lambda

Say you havea large text file for processing.

You could go through line by line and process/validate each line.

The idea here is to break up large files into smaller chunks, and process each chunk using lambda

In this project, I used a sample csv file with 5 million lines.

I have an S3 bucket called maafkn-csv-processor

The only folder I create is one called `raw`.

Once a csv file is copied there, the chain reaction starts.

- The `chunk` lambda separates the file saved to `raw` into lines of 10,000 and saves to the `chunked` folder
- Once a file is saved in `chunked`, the `processChunk` lambda opens the file, validates the email address is valid, and encrypts the SSN, then saves to the `processed` folder.
- Once a file is saved to the `processed` folder, the `saveChunk` lambda kicks in and adds to a Postgres RDS instance using the [`copy_from`](http://initd.org/psycopg/docs/cursor.html#cursor.copy_from) command
