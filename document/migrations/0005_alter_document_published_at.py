# Generated by Django 3.2.18 on 2023-03-07 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_document_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='published_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
