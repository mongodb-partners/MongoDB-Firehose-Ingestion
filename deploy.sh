#!/bin/bash

sam build && sam deploy

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
aws lambda update-function-configuration \
    --function-name $LambdaAuthorizer \
    --environment "Variables={VALID_KEYS=$ApiKeyValue}"

aws apigateway update-method --rest-api-id $ServerlessRestAPI \
    --resource-id $ApiResourceId \
    --http-method ANY \
    --patch-operations op=replace,path=/apiKeyRequired,value=false
