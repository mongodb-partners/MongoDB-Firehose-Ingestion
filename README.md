## Project Overview
---
This is a serverless Python application that helps you to push data from Kinesis Data Firehose to your MongoDB Atlas cluster. This project utilizes AWS Lambda as a resolver to push data into the Atlas cluster. The data flows in the Lambda from an API Gateway through the medium of a Kinesis Data Firehose stream.

### Prerequisites
---
Before proceeding, ensure you have the following prerequisites installed:
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Create IAM User for AWS CLI, Create Access Keys & secret keys
- Configure AWS CLI using `aws configure` with Account Id, Access Key, Secret Key, and Region
- [Install SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- This application requires a minimum version of Python 3.10 to run. You can install Python 3.10 from [Install Python](https://www.python.org/downloads/)

### Usage 
---
#### Deploy Lambda functions and API Gateway

Below mentioned commands will help you deploy the AWS Lambda functions and API Gateway required for the project:

- Run `sam build` & `sam deploy --capabilities CAPABILITY_NAMED_IAM` commands on your terminal
- Run the `deploy.sh` shell script

#### Create a Kinesis Data Firehose Stream
You have to create a Kinesis Data Firehose stream that will help in moving the data from configured source to destination:

- Click [here](https://us-east-1.console.aws.amazon.com/firehose/home?region=us-east-1#/streams) to go to Kinesis Data Firehose console
- Click on `Create Firehose stream`
- Select your desired source of data using the `Source` dropdown
- Select `HTTP Endpoint` option in the `Destination` dropdown
- Enter the API Gateway URL that we created in the previous step in the `HTTP Endpoint URL` field
- Copy the API Key value generated in the previous step and paste it in the `Access Key` field
- Under the `Backup Settings` section, configure a S3 bucket to store the source record backup if the data transformation doesn't produce the desired results
