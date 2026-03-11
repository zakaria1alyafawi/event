import logging
from functools import wraps
import uuid
from datetime import date

# Set up logging
logger = logging.getLogger('Models.Utility')

def validate_string(value, field_name, max_length=None):
    """
    Validate a string field.
    """
    if not value or not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string.")
    if max_length and len(value) > max_length:
        raise ValueError(f"{field_name} must not exceed {max_length} characters.")
    return value

def validate_integer(value, field_name):
    """
    Validate an integer field.
    """
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")
    return value

def validate_json(value, name, item_type=None):
    """
    Validates that a value is a list and optionally checks the type of its elements.
    """
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list, got {type(value).__name__} instead.")

    if item_type:
        for item in value:
            if not isinstance(item, item_type):
                raise ValueError(f"All items in {name} must be of type {item_type.__name__}, but got {type(item).__name__}.")
    return value

def validate_float(value, field_name):
    """
    Validates that the provided value is a float and raises an error if not.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid float. Got {value}.")

def validate_uuid(value, field_name, optional=False):
    """
    Validate a UUID field.
    """
    if optional and value is None:
        return None
    try:
        return uuid.UUID(str(value))
    except ValueError:
        raise ValueError(f"{field_name} must be a valid UUID. Got '{value}'.")

def validate_bool(value, field_name):
    """
    Validate a boolean field.
    """
    if isinstance(value, bool):
        return value
    str_val = str(value).lower()
    if str_val in ('true', '1', 'yes', 'y'):
        return True
    if str_val in ('false', '0', 'no', 'n'):
        return False
    raise ValueError(f"{field_name} must be a boolean value (true/false, 1/0, yes/no). Got '{value}'.")

def validate_date(value, field_name):
    """
    Validate a date field (ISO format).
    """
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} must be ISO date format YYYY-MM-DD. Got '{value}'.")

def validate_enum(value, field_name, allowed_values):
    """
    Validate enum string in allowed values.
    """
    if value not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}. Got '{value}'.")
    return value

def handle_errors(func):
    """
    Decorator for error handling in CRUD operations.
    Logs errors and re-raises them for consistent behavior.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise
    return wrapper
