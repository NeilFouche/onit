"""
A library to manage the retrieval of credentials
"""

import json
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, region="af-south-1", default=None):
    """
    Retrieve a secret from AWS Secrets Manager

    :param secret_name: The name of the secret to retrieve
    :param region: The region in which the secret is stored
    :return: The secret value
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response.get('SecretString', None)
    if secret is None:
        return default

    return json.loads(secret).get(secret_name, default)
