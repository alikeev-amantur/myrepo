from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.fields import GeometryField

from .models import Establishment
from .utils import phone_number_validation


# @establishment_serializer_schema
class EstablishmentSerializer(serializers.ModelSerializer):
    """
    Main serializer for Establishment model
    """
    location = GeometryField()

    class Meta:
        model = Establishment
        fields = (
            "id",
            "name",
            "location",
            "description",
            "phone_number",
            "logo",
            "address",
            "happyhours_start",
            "happyhours_end",
            "owner",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.logo != "":
            return request.build_absolute_uri(obj.logo.url)
        return ""

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["logo"] = self.get_image_url(instance)
        representation["owner"] = instance.owner.email
        return representation


# @establishment_serializer_schema
class EstablishmentCreateUpdateSerializer(serializers.ModelSerializer):
    location = GeometryField()

    class Meta:
        model = Establishment
        fields = (
            "id",
            "name",
            "location",
            "description",
            "phone_number",
            "logo",
            "address",
            "happyhours_start",
            "happyhours_end",
            "owner",
        )

    def validate_location(self, value):
        """Validate that location contains valid latitude and longitude."""
        if value:
            # Check if it's a Point instance
            if not isinstance(value, Point):
                raise serializers.ValidationError("Location must be a valid Point.")

            # Extract latitude and longitude
            latitude, longitude = value.coords[1], value.coords[0]

            # Validate latitude
            if not -90 <= latitude <= 90:
                raise serializers.ValidationError("Latitude must be between -90 and 90.")

            # Validate longitude
            if not -180 <= longitude <= 180:
                raise serializers.ValidationError("Longitude must be between -180 and 180.")

        return value

    def validate_owner(self, value):
        """
        Validate that the owner is the authenticated user.
        """
        user = self.context['request'].user
        if value != user:
            raise serializers.ValidationError("You are not allowed to set the owner to another user.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `Establishment` instance.
        """
        user = self.context['request'].user
        validated_data['owner'] = user
        phone_number_validation(validated_data)
        establishment = Establishment.objects.create(**validated_data)
        return establishment

    def update(self, instance, validated_data):
        """
        Update existing Establishment instance.
        :param instance:
        :param validated_data:
        :return:
        """
        phone_number_validation(validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
