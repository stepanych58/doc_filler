# Generated by Django 2.2.3 on 2019-08-04 19:19

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_passport'),
    ]

    operations = [
        migrations.CreateModel(
            name='SNILS',
            fields=[
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='clients.Client')),
                ('info', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='passport',
            name='id',
        ),
        migrations.AlterField(
            model_name='passport',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='clients.Client'),
        ),
    ]
