from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_deadline(deadline):
    """Validates deadline field, still allows None value."""
    if deadline and deadline <= now():
        raise ValidationError('The deadline field must be set in the future.')