from django.db import models
from accounts.models import Volunteer, Child, Manager


class Pair(models.Model):
    stateChoices = [('0', '待确认'), ('1', '活跃中'), ('2', '结束')]

    volenteer = models.ForeignKey(Volunteer, on_delete=models.PROTECT, verbose_name="志愿者")
    chile = models.ForeignKey(Child, on_delete=models.PROTECT, verbose_name="留守儿童")
    date = models.DateField(auto_now_add=True, verbose_name="结对日期")
    deadline = models.DateField(blank=True, null=True, verbose_name="截止日期")
    state = models.CharField(max_length=1, choices=stateChoices, default='0', verbose_name="结对状态")

    class Meta:
        verbose_name = '结对情况'
        verbose_name_plural = verbose_name

        permissions = (
            ('update_pair_state', '可以修改结对的状态信息'),
        )


class Plan(models.Model):
    typeChoices = [('0', '未分类'), ('1', '生涯'), ('2', '学校'), ('3', '情感')]

    pair = models.ForeignKey(Pair, on_delete=models.PROTECT, verbose_name="结对")
    title = models.CharField(max_length=30, verbose_name="标题")
    date = models.DateField(auto_now_add=True, verbose_name="创建日期")
    type = models.CharField(max_length=1, choices=typeChoices, default='0', verbose_name="类型")
    plan = models.TextField(blank=True, null=True, verbose_name="计划")
    achievment = models.TextField(blank=True, null=True, verbose_name="成果")

    class Meta:
        verbose_name = '帮扶计划'
        verbose_name_plural = verbose_name

