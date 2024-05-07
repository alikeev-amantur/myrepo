from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

establishment_serializer_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Establishment Retrieval Success",
            description="Successful retrieval of an establishment",
            value={
                "id": 1,
                "name": "Joe's Bar",
                "location": "Downtown",
                "description": "Popular local bar with craft beers and live music.",
                "phone_number": "123-456-7890",
                "logo": "http://example.com/media/establishment_logos/joesbar.jpg",
                "address": "123 Main St, Anytown",
                "happyhours_start": "17:00",
                "happyhours_end": "19:00",
                "owner": "owner@example.com",
                "qr_code": {
                    "id": 101,
                    "qr_code_image": "http://example.com/media/qrcodes/joesbar_qr.jpg",
                },
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Establishment Creation Success",
            description="Successful creation of an establishment",
            value={
                "id": 2,
                "name": "The New Place",
                "location": "Uptown",
                "description": "A new trendy spot for evening hangouts.",
                "phone_number": "987-654-3210",
                "logo": "http://example.com/media/establishment_logos/newplace.jpg",
                "address": "456 Side St, Othertown",
                "happyhours_start": "18:00",
                "happyhours_end": "20:00",
                "owner": "owner@example.com",
                "qr_code": {
                    "id": 102,
                    "qr_code_image": "http://example.com/media/qrcodes/newplace_qr.jpg",
                },
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Establishment Update Success",
            description="Successful update of an establishment",
            value={
                "id": 1,
                "name": "Joe's Bar Updated",
                "location": "Downtown",
                "description": "Now featuring a wide selection of imported beers.",
                "phone_number": "123-456-7890",
                "logo": "http://example.com/media/establishment_logos/joesbar_updated.jpg",
                "address": "123 Main St, Anytown",
                "happyhours_start": "17:00",
                "happyhours_end": "21:00",
                "owner": "owner@example.com",
                "qr_code": {
                    "id": 101,
                    "qr_code_image": "http://example.com/media/qrcodes/joesbar_updated_qr.jpg",
                },
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Establishment Update Error",
            description="Error during the update of an establishment due to unauthorized access",
            value={"owner": ["You are not allowed to set the owner to another user."]},
            response_only=True,
        ),
    ]
)
menu_serializer_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Menu Retrieval Success",
            description="Successful retrieval of an establishment's menu including beverages",
            value={
                "id": 1,
                "name": "Joe's Bar",
                "location": "Downtown",
                "description": "Popular local bar with craft beers and live music.",
                "phone_number": "123-456-7890",
                "address": "123 Main St, Anytown",
                "logo": "http://example.com/media/establishment_logos/joesbar.jpg",
                "happyhours_start": "17:00",
                "happyhours_end": "19:00",
                "beverages": [
                    {
                        "id": 1,
                        "name": "Cola",
                        "price": 2.50,
                        "description": "Refreshing carbonated soft drink.",
                        "availability_status": True,
                        "category_name": "Soft Drinks",
                        "establishment_name": "Joe's Bar",
                    },
                    {
                        "id": 2,
                        "name": "Lemonade",
                        "price": 1.75,
                        "description": "Freshly squeezed lemonade.",
                        "availability_status": True,
                        "category_name": "Non-alcoholic",
                        "establishment_name": "Joe's Bar",
                    },
                ],
            },
            response_only=True,
        )
    ]
)
