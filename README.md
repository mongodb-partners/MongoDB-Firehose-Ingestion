## Project Overview
---
This is a serverless Python application that helps you to push data from Kinesis Data Firehose to your MongoDB Atlas cluster. This project utilizes AWS Lambda as a resolver to push data into the Atlas cluster. The data flows in the Lambda from an API Gateway through the medium of a Kinesis Data Firehose stream.

### Prerequisites
---
Before proceeding, ensure you have the following prerequisites in place:
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Create IAM User for AWS CLI, Create Access Keys & secret keys
- Configure AWS CLI using `aws configure` with Account Id, Access Key, Secret Key, and Region
- [Install SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- This application requires a minimum version of Python 3.9 to run. You can install Python 3.9 from [Install Python](https://www.python.org/downloads/)
- A Firehose Stream that will help you move data from source to destination. For this case, our source is `Direct PUT` and destination is `HTTP Endpoint`. To create your Firehose stream, refer [documentation](https://docs.aws.amazon.com/firehose/latest/dev/basic-create.html)

#### Create a Kinesis Data Firehose Stream
You have to create a Kinesis Data Firehose stream that will help in moving the data from configured source to destination:

- Click [here](https://us-east-1.console.aws.amazon.com/firehose/home?region=us-east-1#/streams) to go to Kinesis Data Firehose console
- Click on `Create Firehose stream`
- Select your desired source of data using the `Source` dropdown
- Select `HTTP Endpoint` option in the `Destination` dropdown
- Enter the API Gateway URL that we created in the previous step in the `HTTP Endpoint URL` field
- Copy the API Key value generated in the previous step and paste it in the `Access Key` field
- Under the `Backup Settings` section, configure a S3 bucket to store the source record backup if the data transformation doesn't produce the desired results

### Usage 
---

#### Deploy the serverless application

- Go to Lambda section in your AWS console
- Click on the `Applications` section present on the left navigation bar and then click on **Create application**
- Type **MongoDB-Firehose-Ingestion-App** in the search bar and check the "Show apps that create custom IAM roles or resource policies" checkbox
![Create-App-search-bar](/images/Create-Application-Search.png)
- Fill in the required information and click on **Deploy**
![Deploy-App](/images/Deploy-App.png)
- Go to **Outputs** section of your stack in the cloudformation console and check the outputs of the resources deployed. Keep this tab open
![CF-stack-output](/images/CF-Stack-Output.png)
- Copy the API Key ID mentioned in the Value column alongside the **ApiKeyValue** key. Go to the **Lambda > Select the Authorizer Lambda function > Environment Variables > Paste the copied API Key ID there**
- Go to API Gateway console, click on **Resources > ANY > Click on Edit under Method request settings**. Disable the `API key required` flag. After saving the changes, **Deploy API** for `Prod` stage for the changes to take effect
![API-Key-required](/images/APi-Key-Reqd-Flag.png)
- Copy the **API Gateway endpoint URL for Prod stage** from the cloudformation Outputs section and copy the **API Key value** from the **API Keys** section in the API Gateway
![Copy-API-Key](/images/Copy-API-Key.png)
- Go to the Firehose console and click on the stream that you created then go to **Configuration > Under the Destination Settings** section click on **Edit**. Paste the **API Key Value** and the **API Gateway Web Endpoint** in the fields highlighted below and click on Save changes
![Firehose-Destination-Settings](/images/Firehose-Destination-Settings.png)
- In your Firehose stream, click on **Start sending demo data** under the **Test with demo data** section
![Test-with-demo-data](/images/Test-with-demo-data.png)
- Go to your MongoDB Atlas cluster and check whether you're able to see the records being inserted in your collection

### Note
- For demo purposes, we have allowed access from anywhere `(0.0.0.0/0)` under the Network Access section of MongoDB Atlas Project. We would strictly not recommend this for production scenarios. For production usage, kindly establish a [Private Endpoint](https://www.mongodb.com/docs/atlas/security-cluster-private-endpoint/#follow-these-steps). 