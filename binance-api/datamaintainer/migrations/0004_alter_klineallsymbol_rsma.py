# Generated by Django 3.2.18 on 2023-05-07 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamaintainer', '0003_alter_klineallsymbol_rsma_200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klineallsymbol',
            name='rsma',
            field=models.DecimalField(db_column='rsma', decimal_places=14, default=None, max_digits=32, null=True),
        ),
    ]
