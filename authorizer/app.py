import json
import os
import logging

# Configure logger
logger = logging.getLogger('mongodb_authorizer')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Got Event: {event} ")
    # Extract the custom header
    custom_header = event['headers'].get('X-Amz-Firehose-Access-Key')
    
    # List of valid API keys
    valid_api_keys = os.environ['VALID_KEYS']  # Replace with actual keys

    # Validate the API key
    if custom_header == valid_api_keys:
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
    logger.info("Auth Reponse: ", auth_response)
    return auth_response