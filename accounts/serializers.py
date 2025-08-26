from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "is_staff",
            "password",
            "is_active",
            "organization",
            "photo",
            "phone",
            "role",
        )
        extra_kwargs = {"password": {"write_only": True}}


class AccountReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")
    fullname = serializers.CharField(source="get_full_name")

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        exclude = ["password"]
