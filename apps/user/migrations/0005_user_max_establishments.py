

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="max_establishments",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Maximum number of establishments this user can own",
            ),
        ),
    ]
