import json
import re
import sys
from typing import Any, Callable

def to_camel_case(text: str) -> str:
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


def camel_to_snake(name: str) -> str:
    """
    Converts a camel case or Pascal case string to snake case.

    Args:
        name (str): The name to convert.

    Returns:
        str: The name in snake case.
    """
    # Add underscores before uppercase letters and convert them to lowercase
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def kebab_to_camel(name: str) -> str:
    """
    Converts a kebab case string to camel case.

    Args:
        name (str): The name to convert.

    Returns:
        str: The name in camel case.
    """
    # Add underscores before uppercase letters and convert them to lowercase
    return ''.join(word.capitalize() for word in name.split('-'))

def format_str(
    input_str: str,
    case_function: Callable[[str], str] = str.lower,
    sep: str = "",
    target_sep: str = ""
) -> str:
    """
    Generic string formatter that converts between different casing styles.

    Args:
        input_str: The string to be converted (e.g., "myVariableName").
        case_function: The method to apply to each part (e.g., str.capitalize, str.lower).
            Defaults to str.lower.
        sep: The separator currently in the string (e.g., "_", "-"). Defaults to "" to
            trigger camelCase/PascalCase splitting.
        target_sep: The separator to use in the output (e.g., "_", "-"). Defaults to "".

    Returns:
        The formatted string.
    """
    if not sep:
        collision_safe_delim = chr(31)
        parts = re.sub(r'(?<!^)(?=[A-Z])', collision_safe_delim, input_str).split(collision_safe_delim)
    else:
        parts = input_str.split(sep)

    return target_sep.join([case_function(part) for part in parts])

def format_value(value: str, dtype: str) -> Any:
    type_map = {
        'int': int,
        'float': float,
        'bool': lambda x: str(x).lower() in ('true', '1', 't', 'y'),
        'str': str,
        'list': list,
        'json': json.loads
    }

    caster = type_map.get(dtype)

    if caster is None:
        return value

    try:
        if dtype == 'json':
            value = value.replace("'", '"')
        converted_value = caster(value)
        return converted_value
    except Exception as e:
        print(f"Error casting '{value}' to '{dtype}': {e}", file=sys.stderr)
        return value
