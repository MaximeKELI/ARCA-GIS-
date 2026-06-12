from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_is_2fa_enabled_user_preferred_language_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_2fa_enabled",
            field=models.BooleanField(db_default=False, default=False),
        ),
    ]
