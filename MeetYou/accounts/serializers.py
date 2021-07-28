from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

import rest_framework.serializers as serializers
from meetYou.relations import GenericRelatedField

from accounts.models import Volunteer, Child, Manager, Organization, User, AdminDiv


class StringRelatedWritableField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', None)
        super().__init__(**kwargs)

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class AdminDivSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDiv
        fields = ("id", "name", "code")


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        if mode is not None:
            modeConfig = self.Meta.modes[mode]
            for key, value in modeConfig.items():
                setattr(self.Meta, key, value)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)


class VolunteerSerializer(DynamicFieldsModelSerializer):
    adminDiv = StringRelatedWritableField(queryset=AdminDiv.objects.all())

    class Meta:
        model = Volunteer
        fields = "__all__"
        modes = {
            "create": {
                "read_only_fields": ['id']
            },
            "change_personal_info": {
                "read_only_fields": ['id', 'name', 'cardNum', 'adminDiv', 'schoolId', 'college', 'major']
            },
            "manager_change_info": {
                "read_only_fields": ['id']
            }
        }


class ChildSerializer(DynamicFieldsModelSerializer):
    adminDiv = StringRelatedWritableField(queryset=AdminDiv.objects.all())

    class Meta:
        model = Child
        fields = "__all__"
        modes = {
            "create": {
                "read_only_fields": ['id']
            },
            "change_personal_info": {
                "read_only_fields": ['id', 'name', 'cardNum', 'adminDiv', 'school', 'isProxy']
            },
            "manager_change_info": {
                "read_only_fields": ['id']
            }
        }


class ManagerSerializer(DynamicFieldsModelSerializer):
    adminDiv = StringRelatedWritableField(queryset=AdminDiv.objects.all())

    class Meta:
        model = Manager
        fields = "__all__"
        modes = {
            "create": {
                "read_only_fields": ['id']
            },
            "change_personal_info": {
                "read_only_fields": ['id', 'name', 'cardNum', 'adminDiv']
            },
            "manager_change_info": {
                "read_only_fields": ['id']
            }
        }


class RoleObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Child):
            serializer = ChildSerializer(value)
        elif isinstance(value, Volunteer):
            serializer = VolunteerSerializer(value)
        elif isinstance(value, Manager):
            serializer = ManagerSerializer(value)
        else:
            raise Exception('Unexpected type of role object')

        return serializer.data


# 可以用于获取用户基本信息和用户注册
# 不可以用于修改用户信息！因为没有权限验证，可修改的字段不受限，存在安全风险
class UserSerializer(serializers.ModelSerializer):
    role_object = GenericRelatedField({
        Volunteer: VolunteerSerializer,
        Child: ChildSerializer,
        Manager: ManagerSerializer,
        "volunteer": VolunteerSerializer,
        "child": ChildSerializer,
        "manager": ManagerSerializer,
    })

    class Meta:
        model = User
        fields = ["username", "password", "organization", "role_object"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop("role_object")
        role = role.save()
        user = User.objects.create_user(role_object=role, **validated_data)
        return user


# 仅用于校验密码格式正确性
class PasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField(max_length=16)


class OrganizationSerializer(DynamicFieldsModelSerializer):
    adminDiv = StringRelatedWritableField(queryset=AdminDiv.objects.all())

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['id', "inviteCode", "isActive"]
        modes = {
            "create": {
                "read_only_fields": ['id', "inviteCode", "isActive"]
            },
            "change": {
                "read_only_fields": ['id', "inviteCode", "isActive", "administrator"]
            },
        }
