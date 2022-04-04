from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True, )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class EditProfileSerializer(serializers.ModelSerializer):
    """Сериализатор редактирования профиля пользователя."""
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())], )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(f"Username can't be called 'me'")
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
