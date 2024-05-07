from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

client_registration_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Client User Registration Success",
            description="Successful Client Registration",
            value={
                "id": 1,
                "email": "customer@mail.com",
                "name": "Customer Name",
                "date_of_birth": "2024-04-30",
                "avatar": "null",
                "tokens": {
                    "refresh": "supersecretrefreshtoken",
                    "access": "supersecretaccesstoken",
                },
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Client User Registration Error",
            description="Failed Client Registration (email duplicate)",
            value={"email": ["This field must be unique."]},
            response_only=True,
        ),
    ]
)

partner_creation_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Partner Create Success",
            description="Successful Partner Create",
            value={
                "id": 1,
                "email": "partner@example.com",
                "name": "Partner",
                "max_establishments": 3,
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Partner Create Error",
            description="Failed Partner Create",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
        ),
    ]
)

user_profile_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Client Profile Retrieval",
            description="Successful Client Profile Retrieve",
            value={
                "id": 1,
                "email": "customer@mail.com",
                "name": "null",
                "role": "client",
                "max_establishments": 1,
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Client Profile Updating",
            description="Successful Client Profile Update",
            value={
                "id": 1,
                "email": "customer@mail.com",
                "name": "Customer Name",
                "date_of_birth": "2020-01-01",
                "avatar": "http://example.com/media/client_avatar/customer.jpg",
            },
            response_only=True,
        ),
    ]
)

client_partner_login = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Client/Partner User Login",
            description="Successful Client Login",
            value={
                "refresh": "supersecretrefreshtoken",
                "access": "supersecretaccesstoken",
                "id": 1,
                "email": "customer@mail.com",
                "name": "null",
                "role": "client",
                "max_establishments": 1,
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Client/Partner User Login Error",
            description="Failed Client/Partner Login",
            value={"detail": "No active account found with the given credentials"},
            response_only=True,
        ),
        OpenApiExample(
            name="Client/Partner User Login Error",
            description="Failed Client/Partner Login (blocked)",
            value={"non_field_errors": ["busta straight busta"]},
            response_only=True,
        ),
    ]
)

admin_login_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Admin Login Success",
            description="Successful Admin Login",
            value={
                "refresh": "supersecretrefreshtoken",
                "access": "supersecretaccesstoken",
                "id": 1,
                "email": "admin@mail.com",
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Admin Login Error",
            description="Failed Admin Login",
            value={"non_field_errors": ["Not admin user"]},
            response_only=True,
        ),
    ]
)

admin_block_user_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Admin Block User",
            description="Successful Admin Block User",
            value={"Successful"},
            response_only=True,
        ),
        OpenApiExample(
            name="Admin Block User Error",
            description="Failed Admin Block User",
            value={"non_field_errors": ["User does not exists"]},
            response_only=True,
        ),
    ]
)

user_logout_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="User Logout Success",
            description="Successful Client/Partner Logout",
            value={},
            response_only=True,
        ),
        OpenApiExample(
            name="User Logout Error",
            description="Failed Client/Partner Logout",
            value={"detail": "Token is invalid or expired", "code": "token_not_valid"},
            response_only=True,
        ),
    ]
)

user_password_forgot_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="User Password Forgot Success",
            description="Successful User Password Forgot",
            value={"Success"},
            response_only=True,
        ),
        OpenApiExample(
            name="User Password Forgot Error",
            description="Failed User Password Forgot",
            value={"non_field_errors": ["User does not exists"]},
            response_only=True,
        ),
    ]
)

user_password_reset_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="User Password Reset Success",
            description="Successful User Password Reset",
            value={"Success"},
            response_only=True,
        ),
        OpenApiExample(
            name="User Password Reset Error",
            description="Failed User Password Reset",
            value={"non_field_errors": ["User does not exists"]},
            response_only=True,
        ),
    ]
)

user_password_change_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="User Password Change Success",
            description="Success User Password Change",
            value={"Password successfully changed"},
            response_only=True,
        ),
        OpenApiExample(
            name="User Password Change Error",
            description="Failed User Password Change",
            value={"non_field_errors": ["Passwords do not match"]},
            response_only=True,
        ),
    ]
)

client_list_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Client List Success",
            description="Successful Client List",
            value={
                "count": 1,
                "next": "http://api.example.org/accounts/?offset=400&limit=100",
                "previous": "http://api.example.org/accounts/?offset=200&limit=100",
                "results": [
                    {
                        "id": 1,
                        "email": "customer@example.com",
                        "name": "Customer Name",
                        "date_of_birth": "2024-04-30",
                        "avatar": "http://api.example.com/media/client_avatars/customer_photo.jpg",
                        "is_blocked": "false",
                    }
                ],
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Client List Error",
            description="Failed Client List",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
        ),
    ]
)

partner_list_schema = extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Partner List Success",
            description="Successful Partner List",
            value={
                "count": 1,
                "next": "http://api.example.org/accounts/?offset=400&limit=100",
                "previous": "http://api.example.org/accounts/?offset=200&limit=100",
                "results": [
                    {
                        "id": 0,
                        "email": "partner@example.com",
                        "name": "Partner",
                        "max_establishments": 3,
                        "is_blocked": "false",
                    }
                ],
            },
            response_only=True,
        ),
        OpenApiExample(
            name="Partner List Error",
            description="Failed Partner List",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
        ),
    ]
)
