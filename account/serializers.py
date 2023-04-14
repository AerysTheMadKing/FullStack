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


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)

    default_error_messages = {
        'bad_code': _('Link is expired or invalid!')
    }


    def validate(self, attrs):
        self.code = attrs['code']
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.code)
            user.is_active = True
            user.activation_code = ''
            user.save()

        except User.DoesNotExist:

            self.fail('bad_code')


