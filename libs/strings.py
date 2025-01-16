import re


def to_camel_case(text):
    """
    Converts a sentence or phrase into camel case.

    Args:
        text (str): The text to convert.

    Returns:
        str: The text in camel case.
    """
    # Remove invalid characters (keep only alphanumeric, spaces, and delimiters)
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '', text)

    # Split the sanitized string into words
    words = re.split(r'[-_\s]', sanitized)

    # Convert the first word to lowercase and the rest to title case (capitalized)
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


def camel_to_snake(name):
    """
    Converts a camel case or Pascal case string to snake case.

    Args:
        name (str): The name to convert.

    Returns:
        str: The name in snake case.
    """
    # Add underscores before uppercase letters and convert them to lowercase
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def kebab_to_camel(name):
    """
    Converts a kebab case string to camel case.

    Args:
        name (str): The name to convert.

    Returns:
        str: The name in camel case.
    """
    # Add underscores before uppercase letters and convert them to lowercase
    return ''.join(word.capitalize() for word in name.split('-'))
