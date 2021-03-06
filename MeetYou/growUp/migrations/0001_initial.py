# Generated by Django 2.2.18 on 2021-02-07 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_organization_administrator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='结对日期')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='截止日期')),
                ('state', models.CharField(choices=[('0', '待确认'), ('1', '活跃中'), ('2', '结束')], default='0', max_length=1, verbose_name='结对状态')),
                ('chile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.Child', verbose_name='留守儿童')),
                ('volenteer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.Volunteer', verbose_name='志愿者')),
            ],
            options={
                'verbose_name': '结对情况',
                'verbose_name_plural': '结对情况',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('date', models.DateField(auto_now_add=True, verbose_name='创建日期')),
                ('type', models.CharField(choices=[('0', '未分类'), ('1', '生涯'), ('2', '学校'), ('3', '情感')], default='0', max_length=1, verbose_name='类型')),
                ('plan', models.TextField(blank=True, null=True, verbose_name='计划')),
                ('achievment', models.TextField(blank=True, null=True, verbose_name='成果')),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='growUp.Pair', verbose_name='结对')),
            ],
            options={
                'verbose_name': '帮扶计划',
                'verbose_name_plural': '帮扶计划',
            },
        ),
    ]
