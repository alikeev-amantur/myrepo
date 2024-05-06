from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a superuser from the command line."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="The email of the new superuser.")
        parser.add_argument(
            "password", type=str, help="The password for the new superuser."
        )

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]
        user = get_user_model()

        if not user.objects.filter(email=email).exists():
            user.objects.create_superuser(email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser with email {email}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"A user with the email {email} already exists.")
            )
