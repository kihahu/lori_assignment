from django.core.exceptions import ValidationError

def validate_name(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

def validate_phone(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

def validate_address(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

