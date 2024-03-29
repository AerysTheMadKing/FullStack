from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'last_name', 'first_name', 'username', 'avatar')

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password did not match!')
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('Password fields must contain alpha or numeric types')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    forgot_password_reset = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=30, min_length=8, write_only=True)
    password_confirm = serializers.CharField(required=True, max_length=30, min_length=8, write_only=True)
    default_error_messages = {
        'bad_code': _('Code is expired or invalid!')
    }

    def validate(self, attrs):
        self.forgot_password_reset = attrs['forgot_password_reset']
        password_confirm = attrs.pop('password_confirm')
        password = attrs['password']

        if password_confirm != password:
            raise serializers.ValidationError(
                'Passwords didn\'t match!'
            )
        if password == User.password:
            raise serializers.ValidationError(
                'Password field must contain alpha and numeric'
            )
        user = User.objects.get(forgot_password_reset=attrs['forgot_password_reset'])
        user.set_password(password)
        user.save()
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(forgot_password_reset=self.forgot_password_reset)
            user.forgot_password_reset = ''
            user.save()
        except User.DoesNotExist:
            self.fail('bad_password')
