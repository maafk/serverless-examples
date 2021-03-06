# Snapshot EBS volumes (AWS SAM)

This project will create EBS snapshots for all volumes attached to EC2 instances that have a tag of 'backup'

It will run on a schedule Monday-Friday.

## Setup

- Install [SAM Local](https://github.com/awslabs/aws-sam-local)

## Package and deploy application

```
$ sam package --template-file template.yml --s3-bucket my-bucket --s3-prefix snapshot-ebs --output-template-file template-deploy.yml
$ sam deploy --template-file /path/to/template-deploy.yml --stack-name snapshot-ebs --capabilities CAPABILITY_IAM
```