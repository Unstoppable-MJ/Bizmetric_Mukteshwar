from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ["id", "username", "email", "phone", "password"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = validated_data.pop("password")

        user = User.objects.create(
            username=user_data["username"],
            email=user_data["email"],
        )
        user.set_password(password)
        user.save()

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.get("user", {})
        instance.user.username = user_data.get("username", instance.user.username)
        instance.user.email = user_data.get("email", instance.user.email)
        instance.user.save()

        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        return instance