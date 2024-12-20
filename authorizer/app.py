import json
import os

def lambda_handler(event, context):
    # Extract the custom header
    custom_header = event['headers'].get('X-Amz-Firehose-Access-Key')
    
    # List of valid API keys
    valid_api_keys = os.environ['VALID_KEYS']  # Replace with actual keys

    # Validate the API key
    if custom_header == valid_api_keys:
        print('KEY IS VALID')
        return generate_policy('user', 'Allow', event['methodArn'])
    else:
        print('KEY NOT VALID')
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
    print("Auth Reponse: ", auth_response)
    return auth_response