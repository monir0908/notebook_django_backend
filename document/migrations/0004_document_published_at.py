# Generated by Django 3.2.18 on 2023-03-07 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_auto_20230220_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='published_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]