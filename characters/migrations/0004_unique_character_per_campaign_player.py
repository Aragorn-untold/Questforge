from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("characters", "0003_character_items"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="character",
            constraint=models.UniqueConstraint(
                fields=("campaign", "player"),
                name="unique_character_per_player_per_campaign",
            ),
        ),
    ]
