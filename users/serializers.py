from datetime import datetime

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

from common.utils import send_confirmation_email
from .models import User, UserConfirmation


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['theme']


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate_email(self, value):
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code()
        send_confirmation_email(user.email, code)
        user.save()
        return user


class UserConfirmationSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserConfirmation
        fields = ['email', 'code', 'datetime']

    # def update(self, instance, validated_data):
    #     if validated_data['expiration_time'] > datetime.now():
    #         raise serializers.ValidationError("Expiration time is over")
    #     else:
    #         UserConfirmation.objects.filter(user=instance)

