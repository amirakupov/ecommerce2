# Generated by Django 4.2 on 2023-07-05 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_remove_product_alcohol_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='whole_box_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]