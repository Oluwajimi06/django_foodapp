# Generated by Django 4.2.7 on 2023-11-27 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0011_rename_total_amount_paid_order_total_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_amount',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='sitepages.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
