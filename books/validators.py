from django.core.exceptions import ValidationError

def validate_name(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

def validate_description(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

def validate_author(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot blank")
    return value

