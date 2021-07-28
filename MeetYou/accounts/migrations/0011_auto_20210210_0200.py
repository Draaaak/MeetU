# Generated by Django 2.2.18 on 2021-02-09 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210209_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='inviteCode',
            field=models.CharField(blank=True, default='', max_length=8, null=True, verbose_name='邀请码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin', to='accounts.Organization', verbose_name='隶属组织'),
        ),
    ]