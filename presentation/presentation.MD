# Why are we here?

"The whole point of running application software is to deliver business value of some sort" - Adrian Cockcroft

This idea needs to be the underpinning of all we do. "Does this deliver business value?"

We add tools to our software development process that 100% delivers business value as it relates to our development process.

Writing tests for our code, running commits through CI/CD pipelines, automatically proviioning infrastructure.

- Monolith in a data center
  - Legthy procurment process
  - Pre-provision capacity
- Shift to the cloud
  - Instantly have servers available
  - Can plan for auto scaling


![Customers Don't give a shit about your data center][customer_data_center]


---
# What is Serverless?

Serverless != No servers

Short definition: Thinking about servers less

Longer definition: Using a combination of managed services (usually from a cloud provider) to get work done that does't involve a traditional server

---
# Why Serverless?

- Pay for what you use
- Scales effortlessly
- Don't have to manage underlying servers
- Reduce time from concept to production

---
# What Services are there?

Service | What it does
---|---
AWS Lambda | Runs custom code on ephemeral containers
AWS API Gateway | Create an API backed by Lambda
AWS S3 | Object storage and static website hosting
AWS DynamoDB | Manages NoSQL database
AWS Congito | User management and access control
AWS Step Functions | Lambda functions connected by state machines
AWS SNS | Managed PubSub messaging
AWS SQS | Managed message queues
AWS Batch | Run batch computing workloads
AWS Kinesis | Analyze real time streaming data


---
# Demos on what we're currently doing

[cloudops projects]()
- Pingdom Proxy
- Pingdom Proxy Security Groups
- Pingdom FaaS
- 

Show how we use CI/CD

---
# Good reads in prep:

[Evolution of business logic](https://read.acloud.guru/evolution-of-business-logic-from-monoliths-through-microservices-to-functions-ff464b95a44d) by Adrian Cockcroft

[Serverless is just a name](https://serverless.zone/serverless-is-just-a-name-we-could-have-called-it-jeff-1958dd4c63d7) by Paul Johnston

---
# AWS Workshops

[AWS Serverless workshops](https://github.com/aws-samples/aws-serverless-workshops)

---
# Tools

[Serverless](https://serverless.com/framework/docs/providers/aws/) Framework

[AWS SAM](https://github.com/awslabs/serverless-application-model/blob/develop/versions/2016-10-31.md) (Serverless Application Model)

[AWS SAM Local](https://github.com/awslabs/aws-sam-local) - Run SAM locally

[Chalice](https://github.com/aws/chalice/) - Python framework for serverless applications on AWS

[Zappa](https://www.zappa.io/) -  Turn a WSGI application (Django, Flask) to an AWS serverless application

[ClaudiaJs](https://github.com/claudiajs/claudia) - Deploy NodeJS applications as AWS serverless application

[customer_data_center]: img/customers-data-center.png