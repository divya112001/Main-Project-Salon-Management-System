# Generated by Django 3.2.24 on 2024-04-09 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_rentalproduct_table_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalbookingdetails_table',
            name='quantity',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]