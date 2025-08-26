from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group

User = get_user_model()


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):

    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False, allow_empty=True
    )
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False, allow_empty=True
    )

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
            "groups",
            "user_permissions",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])

        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        user.groups.set(groups)
        user.user_permissions.set(user_permissions)
        user.save()
        return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)

        if groups:
            instance.groups.set(groups)

        if user_permissions:
            instance.user_permissions.set(user_permissions)
        instance.save()
        return instance


class AccountReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")
    fullname = serializers.CharField(source="get_full_name")

    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        exclude = ["password"]
