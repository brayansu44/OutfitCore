# Generated by Django 5.2.4 on 2025-07-18 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cuentas', '0013_remove_facturacompra_fecha_vencimiento_and_more'),
        ('Ventas', '0008_remove_ventas_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Cuentas.cliente'),
            preserve_default=False,
        ),
    ]
