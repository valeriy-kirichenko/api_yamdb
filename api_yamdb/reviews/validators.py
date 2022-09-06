from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(year):
    """Проверяет год произведения.

    Args:
        year (int): год произведения.

    Raises:
        ValidationError: ошибка если год произведения больше текущего.
    """

    if not (year <= datetime.now().year):
        raise ValidationError('Год выпуска не может быть больше текущего')
