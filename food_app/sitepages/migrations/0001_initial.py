# Generated by Django 4.2.7 on 2023-11-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc_short', models.CharField(max_length=100)),
                ('desc_long', models.TextField()),
                ('price', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='uploaded')),
            ],
        ),
    ]