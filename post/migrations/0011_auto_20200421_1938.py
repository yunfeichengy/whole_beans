# Generated by Django 3.0.3 on 2020-04-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]
