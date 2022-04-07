from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(year):
    if not (0 < year <= datetime.now().year):
        raise ValidationError('Год выпуска не может быть больше текущего '
                              'или быть отрицательным')
