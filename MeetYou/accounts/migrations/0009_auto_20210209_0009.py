# Generated by Django 2.2.18 on 2021-02-08 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210209_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
        ),
    ]
