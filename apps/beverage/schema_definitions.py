from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
    extend_schema,
)

beverage_serializer_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Create Beverage Success",
            description="Successful creation of a beverage",
            value={
                "name": "Cola",
                "price": 2.50,
                "description": "Refreshing carbonated soft drink.",
                "availability_status": True,
                "category": 1,
                "establishment": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Beverage Retrieval Success",
            description="Successful retrieval of a beverage",
            value={
                "id": 1,
                "name": "Cola",
                "price": 2.50,
                "description": "Refreshing carbonated soft drink.",
                "availability_status": True,
                "category": "Soft Drinks",
                "establishment": "Joe's Bar",
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Beverage Update Success",
            description="Successful update of a beverage",
            value={
                "id": 1,
                "name": "Cola",
                "price": 3.00,
                "description": "Extra refreshing carbonated soft drink.",
                "availability_status": True,
                "category": 1,
                "establishment": 1,
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Beverage Creation Error",
            description="Error during the creation of a beverage due to invalid data",
            value={"price": ["Ensure this value is greater than or equal to 0.01."]},
            response_only=True,
            status_codes=["400"],
        ),
    ]
)
