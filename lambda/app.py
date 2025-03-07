import os
import json
from pymongo import MongoClient
from bson import ObjectId
import base64
import logging
import traceback
import boto3

# Configure logger
logger = logging.getLogger('mongodb_handler')
logger.setLevel(logging.INFO)

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        # Handle specific exceptions as needed
        raise e

    # Secrets Manager can return either a string or binary secret
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return base64.b64decode(get_secret_value_response['SecretBinary']).decode('utf-8')

# Environment variables
ATLAS_CONNECTION_STRING = get_secret(os.environ['SECRET_NAME'], os.environ['REGION_NAME'])
COLLECTION_NAME = os.environ['COLLECTION_NAME']
DB_NAME = os.environ['DB_NAME']

def connect_to_mongodb():
    return MongoClient(ATLAS_CONNECTION_STRING)

# client = MongoClient(host = ATLAS_CONNECTION_STRING)

def success_response(body):
    return {
        'statusCode': '200',
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def error_response(err):
    error_message = str(err)
    return {
        'statusCode': '400',
        'body': error_message,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def decode_base64_builtin(s):
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception as e:
        logger.error(f"Error decoding Base64: {str(e)}")
        return None


def lambda_handler(event, context):
    client = None
    logger.info(f"got event: {event}")
    try:
        logger.info("starting processing event")

        client = connect_to_mongodb()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        logger.info(f"connected to the database...")

        full_document = json.loads(event["body"])
        logger.info(f"got full_document: {full_document}")

        documents_to_insert = []
        for record in full_document['records']:
            # Decode base64 data and parse JSON
            document = json.loads(decode_base64_builtin(record['data']))
            documents_to_insert.append(document)

        # Perform bulk insert if there are documents
        if documents_to_insert:
            status = collection.insert_many(documents_to_insert, ordered=False)
            logger.info(f"Successfully inserted {len(status.inserted_ids)} documents")
            response = {'inserted_count': len(status.inserted_ids)}
        else:
            logger.info("No documents to insert")
            response = {'inserted_count': 0}
        
        logger.info("finished processing event")
        return success_response(response)

    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        logger.error(traceback.format_exc())
        return error_response(e)

    finally:
        if client:
            client.close()
