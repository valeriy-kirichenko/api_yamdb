import re

from rest_framework import serializers


class ValidateMixin(object):
    """Класс примесь для валидации данных."""

    def validate_username(self, username):
        """Проверяет имя пользователя.

        Args:
            username (str): имя пользователя.

        Raises:
            serializers.ValidationError: ошибка если имя пользователя "me".
            serializers.ValidationError: ошибка если имя пользователя не
            соответствует регулярному выражению.

        Returns:
            str: имя пользователя.
        """

        text = 'Недопустимый username: '
        if username == 'me':
            raise serializers.ValidationError(text + username)
        if re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(text + username)
        return username
