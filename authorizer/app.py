import os
import logging
import boto3

# Configure logger
logger = logging.getLogger('mongodb_authorizer')
logger.setLevel(logging.INFO)
# Create API Gateway client
client = boto3.client('apigateway')

def get_api_key_by_id(api_key_id):
    # Get API key details
    response = client.get_api_key(
        apiKey=api_key_id,
        includeValue=True  # Set to True to include the actual key value
    )
    
    return response.get('value')

def lambda_handler(event, context):
    logger.info(f"Got Event: {event} ")
    # Extract the custom header
    custom_header = event['headers'].get('X-Amz-Firehose-Access-Key')
    
    # List of valid API keys
    valid_api_key = get_api_key_by_id(os.environ['API_KEY_ID'])

    # Validate the API key
    if custom_header == valid_api_key:
        logger.info('KEY IS VALID')
        return generate_policy('user', 'Allow', event['methodArn'])
    else:
        logger.info('KEY NOT VALID')
        return generate_policy('user', 'Deny', event['methodArn'])

def generate_policy(principal_id, effect, resource):
    # Generate IAM policy
    auth_response = {
        "principalId": principal_id
    }

    if effect and resource:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
        auth_response['policyDocument'] = policy_document
    logger.info(f"Auth Response: {auth_response}")
    return auth_response