from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# 行政区 administrative divisions
class AdminDiv(models.Model):
    code = models.IntegerField(unique=True, verbose_name="行政区划代码")
    name = models.CharField(max_length=15, unique=True, verbose_name="单位名称")

    class Meta:
        verbose_name = '行政区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AbstractRole(models.Model):
    name = models.CharField(max_length=10, verbose_name="姓名")
    cardNum = models.CharField(max_length=18, unique=True, verbose_name="身份证号")
    adminDiv = models.ForeignKey(AdminDiv, on_delete=models.PROTECT, verbose_name='行政区')
    address = models.CharField(max_length=100, blank=True, null=True, default="", verbose_name="个人住址")
    user = GenericRelation('User')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    
class Volunteer(AbstractRole):
    isActiveChoices = [('0', '不活跃'), ('1', '活跃')]

    schoolId = models.CharField(max_length=10, verbose_name="学号")
    college = models.CharField(max_length=15, verbose_name="学院")
    major = models.CharField(max_length=15, verbose_name="专业")
    description = models.TextField(blank=True, null=True, default="", verbose_name="个人简介")
    isActive = models.CharField(max_length=1, choices=isActiveChoices, default='0', verbose_name="是否处于活跃状态")

    class Meta:
        verbose_name = '志愿者'
        verbose_name_plural = verbose_name

        permissions = (
            ('view_pair', '可以查看结对另一方的信息'),
        )


class Child(AbstractRole):
    isProxyChoices = [('0', '未代理'), ('1', '代理')]
    isActiveChoices = [('0', '不活跃'), ('1', '活跃')]

    school = models.CharField(max_length=15, verbose_name="学校")
    description = models.TextField(blank=True, null=True, default="", verbose_name="个人情况介绍")
    isProxy = models.CharField(max_length=1, choices=isProxyChoices, default='0', verbose_name="是否由村长代理")
    isActive = models.CharField(max_length=1, choices=isActiveChoices, default='0', verbose_name="是否处于活跃状态")

    class Meta:
        verbose_name = '留守儿童'
        verbose_name_plural = verbose_name

        permissions = (
            ('view_pair', '可以查看结对另一方的信息'),
        )


class Manager(AbstractRole):
    description = models.TextField(blank=True, null=True, default="", verbose_name="个人简介")

    class Meta:
        verbose_name = '组织管理员'
        verbose_name_plural = verbose_name


class Organization(models.Model):
    isActiveChoices = [('0', '不活跃'), ('1', '活跃')]

    administrator = models.ForeignKey('User', on_delete=models.PROTECT, related_name="org", verbose_name="管理员")
    adminDiv = models.ForeignKey(AdminDiv, on_delete=models.PROTECT, verbose_name='所处的行政区')
    address = models.CharField(max_length=100, blank=True, null=True, default="", verbose_name="地址")
    description = models.TextField(blank=True, null=True, default="", verbose_name="描述")
    inviteCode = models.CharField(max_length=8, blank=True, null=True, default="", verbose_name="邀请码")
    isActive = models.CharField(max_length=1, choices=isActiveChoices, default="0", verbose_name="是否处于激活状态")

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name

        permissions = (
            ('add_members', '可以添加人员'),
            ('remove_members', '可以移除人员'),
        )


class User(AbstractUser):
    organization = models.ForeignKey(Organization, blank=True, null=True, default="", on_delete=models.SET_NULL, related_name="admin", verbose_name="隶属组织")

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    role_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
