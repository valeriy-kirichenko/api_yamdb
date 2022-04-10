import re

from rest_framework import serializers


class ValidateMixin(object):
    def validate_username(self, username):
        """Валидация username"""
        text = 'Недопустимый username: '
        if username == 'me':
            raise serializers.ValidationError(text + username)
        if re.match(r'^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(text + username)
        return username
