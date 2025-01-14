#!/bin/bash

sam build && sam deploy --capabilities CAPABILITY_NAMED_IAM

STACK_NAME="kinesis-mdb-lambda"

# Get multiple outputs at once
eval $(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output text | while read -r key value; do
    echo "$key='$value'"
done)

# Now you can use the variables directly
echo "API Endpoint: $WebEndpoint"
echo "API Resource ID: $ApiResourceId"
echo "Lambda Authorizer: $LambdaAuthorizer"

# Or get a specific output
API_KEY=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiKeyValue`].OutputValue' \
    --output text)

echo "API Key: $API_KEY"

# update Lambda with the 
echo "updating Lambda Environment Variable for API Key"
aws lambda update-function-configuration \
    --function-name $LambdaAuthorizer \
    --environment "Variables={API_KEY_ID=$ApiKeyValue}"

echo "disabling API Key Required to enable authorizer" 
aws apigateway update-method --rest-api-id $ServerlessRestAPI \
    --resource-id $ApiResourceId \
    --http-method ANY \
    --patch-operations op=replace,path=/apiKeyRequired,value=false

echo "updating Lambda policy to allow access to API Key"
read -r -d '' POLICY_DOCUMENT <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "apigateway:GET",
                "apigateway:GetApiKey"
            ],
            "Resource": "arn:aws:apigateway:us-east-1::/apikeys/$ApiKeyValue"
        }
    ]
}
EOF

aws iam put-role-policy \
  --role-name $AuthorizerLambdaRoleName \
  --policy-name APIGatewayGetKeyPolicy \
  --policy-document "$POLICY_DOCUMENT"

echo "Creating production deployment stage"
aws apigateway create-deployment \
    --rest-api-id $ServerlessRestAPI \
    --stage-name prod \
    --description "Production deployment"

echo "Production API Endpoint: https://$ServerlessRestAPI.execute-api.us-east-1.amazonaws.com/prod/"
