from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ["username", "password"]


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item_name", "item_price", "description"]
