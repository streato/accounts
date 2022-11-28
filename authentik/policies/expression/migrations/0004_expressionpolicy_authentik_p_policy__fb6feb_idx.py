# Generated by Django 4.1.2 on 2022-10-19 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_policies_expression", "0003_auto_20201203_1223"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="expressionpolicy",
            index=models.Index(fields=["policy_ptr_id"], name="authentik_p_policy__fb6feb_idx"),
        ),
    ]
