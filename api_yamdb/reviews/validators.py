from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(title_year):
    if title_year > timezone.now().year:
        raise ValidationError(
            'Указанный год больше текущего!'
        )
    return title_year
