from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.schema_definitions import (
    client_registration_schema,
    partner_creation_schema,
    user_profile_schema,
    client_partner_login,
    admin_login_schema,
    admin_block_user_schema,
    user_password_forgot_schema,
    user_password_reset_schema,
    user_password_change_schema,
    client_list_schema,
    partner_list_schema,
)

User = get_user_model()


@client_partner_login
class TokenObtainSerializer(TokenObtainPairSerializer):
    """
    Token Obtaining Serializer
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get("email"))
            if not user.is_blocked or user.is_superuser:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                data["id"] = user.id
                data["email"] = user.email
                data["name"] = user.name
                data["role"] = user.role
                data["max_establishments"] = user.max_establishments
                return data
            raise serializers.ValidationError("busta straight busta")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")


@admin_login_schema
class AdminLoginSerializer(TokenObtainPairSerializer):
    """
    Token Obtaining Serializer for admin, superuser
    """

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get("email"))
            if user.role == "admin" or user.is_superuser:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                data["id"] = user.id
                data["email"] = user.email
                return data
            raise serializers.ValidationError("Not admin user")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")


@admin_block_user_schema
class BlockUserSerializer(serializers.ModelSerializer):
    """
    Serializer for blocking users
    """

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            "email",
            "is_blocked",
        )

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            user = User.objects.get(email=attrs.get("email"))
            if user.is_blocked == attrs.get("is_blocked"):
                raise serializers.ValidationError("You didn't change block state")
            return attrs
        raise serializers.ValidationError("User does not exists")


@client_registration_schema
class ClientRegisterSerializer(serializers.ModelSerializer):
    """
    Individual register view for client user
    """

    password = serializers.CharField(
        write_only=True, required=True, min_length=8, max_length=255
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "password_confirm",
            "name",
            "date_of_birth",
            "avatar",
        )

    def validate(self, attrs):
        """
        Validating passwords form user input
        :param attrs:
        :return:
        """
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        """
        Creating user with client role
        :param validated_data:
        :return:
        """
        user = User.objects.create_user(role="client", **validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


@user_password_forgot_schema
class ClientPasswordForgotPageSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ("email",)

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            return attrs
        raise serializers.ValidationError("User does not exist")


@user_password_reset_schema
class ClientPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    reset_code = serializers.CharField(max_length=4, required=True)

    class Meta:
        fields = (
            "email",
            "reset_code",
        )

    def validate(self, attrs):
        try:
            User.objects.filter(email=attrs.get("email"))
        except User.DoesNotExist as user_not_exist:
            raise serializers.ValidationError(
                "User does not exists"
            ) from user_not_exist
        return attrs


@user_password_change_schema
class ClientPasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, required=True, max_length=255
    )
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "password",
            "password_confirm",
        )

    def validate(self, attrs):
        """
        Validating passwords form user input
        :param attrs:
        :return:
        """
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs


@user_profile_schema
class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer
    """

    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "date_of_birth",
            "avatar",
        )


@client_list_schema
class ClientListSerializer(serializers.ModelSerializer):
    """
    Only for client list
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "date_of_birth",
            "avatar",
            "is_blocked",
        )


@partner_list_schema
class PartnerListSerializer(serializers.ModelSerializer):
    """
    Only for partner list
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "max_establishments",
            "is_blocked",
        )


@partner_creation_schema
class PartnerCreateSerializer(serializers.ModelSerializer):
    """
    Individual create view for partner user
    """

    password = serializers.CharField(
        write_only=True, required=True, min_length=8, max_length=255
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "password",
            "password_confirm",
            "max_establishments",
        )

    def validate(self, attrs):
        """
        Validating passwords from user input
        :param attrs:
        :return:
        """
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        """
        Creating user with partner role
        :param validated_data:
        :return:
        """
        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            max_establishments=validated_data["max_establishments"],
            role="partner",
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
