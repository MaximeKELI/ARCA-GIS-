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
        migrations.AlterField(
            model_name="user",
            name="preferred_language",
            field=models.CharField(db_default="fr", default="fr", max_length=5),
        ),
        migrations.AlterField(
            model_name="user",
            name="totp_secret",
            field=models.CharField(blank=True, db_default="", default="", max_length=32),
        ),
    ]
