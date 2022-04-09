import re
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                f"Username can't be called {username}")
        if re.match('^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {username}')
        return username


class EditProfileSerializer(UserSerializer):
    """Сериализатор редактирования профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(required=True, max_length=150, )
    email = serializers.EmailField(required=True, max_length=254, )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                f'Запрещено называть Username: {username}')
        return username

    def validate(self, data):
        name_search_in_db = User.objects.filter(username=data.get('username'))
        email_search_in_db = User.objects.filter(email=data.get('email'))
        if name_search_in_db or email_search_in_db:
            raise serializers.ValidationError(f'Дублирование в базе данных!')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    username = serializers.CharField(required=True, max_length=150, )
    confirmation_code = serializers.CharField(required=True, )
