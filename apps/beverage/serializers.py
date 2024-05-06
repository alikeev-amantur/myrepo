from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from .models import Beverage, Category
from .schema_definitions import beverage_serializer_schema
from ..partner.models import Establishment


class CategorySerializer(serializers.ModelSerializer):
    beverages = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="v1:beverage-detail"
    )

    class Meta:
        model = Category
        fields = ["id", "name", "beverages"]


@beverage_serializer_schema
class BeverageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beverage
        fields = [
            "id",
            "name",
            "price",
            "description",
            "availability_status",
            "establishment",
            "category"
        ]

    def to_representation(self, instance):
        """Modify the output of the GET method to show names instead of IDs."""
        ret = super().to_representation(instance)
        ret['category'] = instance.category.name if instance.category else None
        ret['establishment'] = instance.establishment.name if instance.establishment else None
        return ret

    def validate_establishment(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("User does not own this establishment.")
        return value

    def validate_price(self, value):
        """
        Check that the price is not negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                "The price must be a non-negative number."
            )
        return value
