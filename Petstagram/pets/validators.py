from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validate_past_date(value):
    if value > now().date():
        raise ValidationError("The date cannot be in the future.")
