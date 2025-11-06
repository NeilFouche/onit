"""
A library to manage the retrieval of credentials
"""

import os
from dotenv import load_dotenv


def get_secret(secret_name: str, env: str = "production") -> str:
    """
    Returns the specified secret based on the environment.

    During development use the .env for dev values, but use env variables in
    production env. Most hosting providers use standard env ecosystem to manage
    secret values, so the default way to get the secret is reading it from the
    env with os.
    """

    source = 'file' if env == 'development' else 'env'

    if source == 'file':
        return get_file_variable(secret_name, env)

    return get_env_secret(secret_name)

def get_env_secret(secret_name: str, source: str = "railway"):
    """
    Gets the secret value from the source (host) secret variable API
    """

    return os.environ.get(secret_name, "")

def get_file_variable(variable, env) -> str:
    """
    Returns the specified variable value.
    """
    if env not in ["production", "development"]:
        env = "production"

    load_dotenv(f'.env.{env}', override=True)

    return os.getenv(variable, "")
