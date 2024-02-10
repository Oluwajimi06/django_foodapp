# Generated by Django 4.2.7 on 2024-01-15 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0023_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='category',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], default='Breakfast', max_length=10),
        ),
    ]
