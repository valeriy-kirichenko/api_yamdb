from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
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
        return username



class UserSerializer(CustomUserSerializer):
    """Сериализатор пользователя."""


class EditProfileSerializer(CustomUserSerializer):
    """Сериализатор редактирования профиля пользователя."""

    class Meta(CustomUserSerializer.Meta):
        read_only_fields = ('role',)


class RegistrationSerializer(CustomUserSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta(CustomUserSerializer.Meta):
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

