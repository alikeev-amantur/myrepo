from django.utils import timezone
from rest_framework import serializers
from .models import Order
import datetime

from .schema_definitions import order_serializer_schema, order_history_serializer_schema


@order_serializer_schema
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "establishment", "beverage", "client", "order_date"]
        read_only_fields = ["client", "establishment"]

    def get_default_establishment(self, beverage):
        # Get the establishment associated with the beverage
        return beverage.establishment

    def validate_order_happyhours(self, establishment):
        current_time = timezone.localtime().time()
        if not (
            establishment.happyhours_start
            <= current_time
            <= establishment.happyhours_end
        ):
            raise serializers.ValidationError(
                "Order can only be placed during the establishment's designated happy hours."
            )

    def validate_order_per_hour(self, client):
        # Get the current time and calculate one hour ago
        one_hour_ago = timezone.localtime() - datetime.timedelta(hours=1)

        # Check if there are any existing orders from this client in the last hour
        if Order.objects.filter(client=client, order_date__gte=one_hour_ago).exists():
            raise serializers.ValidationError("You can only place one order per hour.")

    def validate_order_per_day(self, client, establishment):
        # Ensure one order per day per establishment
        current_time = timezone.localtime()
        today_min = datetime.datetime.combine(current_time.date(), datetime.time.min)
        today_max = datetime.datetime.combine(current_time.date(), datetime.time.max)

        existing_order_same_day = Order.objects.filter(
            client=client,
            establishment=establishment,
            order_date__range=(today_min, today_max),
        ).exists()

        if existing_order_same_day:
            raise serializers.ValidationError(
                "You can only place one order per establishment per day."
            )

    def validate(self, data):
        # Automate providing client and establishment
        data["client"] = self.context["request"].user
        data["establishment"] = self.get_default_establishment(data["beverage"])

        client = data["client"]
        establishment = data["establishment"]

        self.validate_order_happyhours(establishment)
        self.validate_order_per_day(client, establishment)
        self.validate_order_per_hour(client)

        return data


@order_history_serializer_schema
class OrderHistorySerializer(serializers.ModelSerializer):
    establishment_name = serializers.CharField(
        source="establishment.name", read_only=True
    )
    beverage_name = serializers.CharField(source="beverage.name", read_only=True)

    # client_details = serializers.HyperlinkedRelatedField(
    #     view_name='v1:user-detail',
    #     read_only=True,
    #     source='client'
    # )

    class Meta:
        model = Order
        fields = ["id", "order_date", "establishment_name", "beverage_name"]
