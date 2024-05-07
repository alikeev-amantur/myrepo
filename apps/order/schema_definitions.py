# schema_definitions.py
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
    OpenApiResponse,
    extend_schema,
)
import datetime

order_serializer_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Create Order Success",
            description="Successful creation of an order during happy hours",
            value={
                "beverage": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Create Order Success",
            description="Example of successfully creating an order during happy hours",
            value={
                "beverage": 1,
                "establishment": 1,
                "client": 1,
                "order_date": "2024-04-29T15:00:00Z",
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            name="Create Order Failure - Happy Hours",
            description="Failed attempt to create an order outside happy hours",
            value={"detail": "You can only place an order during happy hours."},
            response_only=True,
            status_codes=["400"],
        ),
        OpenApiExample(
            name="Create Order Failure - Order Frequency",
            description="Failed attempt to create an order due to frequency limit (one per hour/day)",
            value={
                "detail": "You can only place one order per hour and one order per establishment per day."
            },
            response_only=True,
            status_codes=["400"],
        ),
    ]
)

order_history_serializer_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Order History Retrieval Success",
            description="Successful retrieval of order history for a client",
            value=[
                {
                    "id": 1,
                    "order_date": "2024-04-30T17:00:00Z",
                    "establishment_name": "Joe's Bar",
                    "beverage_name": "Cola",
                    "client_details": "http://example.com/api/v1/users/1",
                },
                {
                    "id": 2,
                    "order_date": "2024-04-29T15:00:00Z",
                    "establishment_name": "The Coffee Shop",
                    "beverage_name": "Espresso",
                    "client_details": "http://example.com/api/v1/users/1",
                },
            ],
            response_only=True,
        )
    ]
)
create_order_success = OpenApiExample(
    name="Create Order Success",
    description="Example of successfully creating an order during happy hours",
    value={
        "beverage": 1,
        "establishment": 1,
        "client": 1,
        "order_date": "2024-04-29T15:00:00Z",
    },
    status_codes=["201"],
)
