import re
from django.core.exceptions import ValidationError



def custom_username_validator(value):
    if not re.match(r'^[A-Za-z ]+$', value):
        raise ValidationError("Username can contain only alphabets and spaces")
    words = value.split()
    for word in words:
        if not word[0].isupper():
            raise ValidationError("Each word must start with a capital letter")