from django.db import models
from growUp.models import Plan


class Show(models.Model):
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE, verbose_name="为展示的帮扶")
    comment = models.CharField(max_length=300, blank=True, null=True, verbose_name="评论")

    class Meta:
        verbose_name = '风采展示'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=30, verbose_name="标题")
    date = models.DateTimeField(auto_now_add=True, verbose_name="发表日期")
    body = models.TextField(blank=True, null=True, verbose_name="正文")
    author = models.CharField(max_length=30, verbose_name="作者")
    pv = models.IntegerField(default=0, verbose_name="浏览量")

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
