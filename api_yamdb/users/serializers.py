import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                f"Username can't be called {username}")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с никнеймом {username} уже зарегистрирован')
        elif re.match('^[\w.@+-]+\Z', username) is None:
            raise serializers.ValidationError(
                f'Недопустимое имя пользователя: {username}')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'Email: {email} уже зарегистрирован')
        return email


class EditProfileSerializer(UserSerializer):
    """Сериализатор редактирования профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegistrationSerializer(UserSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta(UserSerializer.Meta):
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], )
    confirmation_code = serializers.CharField()

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                f"Username can't be called {username}")
        return username
