from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django import forms

from rest_framework import serializers

class GenericSerializerMixin(object):
    default_error_messages = {
        'no_model_match': _('Invalid model - model not available.'),
        'no_url_match': _('Invalid hyperlink - No URL match'),
        'incorrect_url_match': _(
            'Invalid hyperlink - view name not available'),
    }

    form_field_class = forms.URLField

    def __init__(self, serializers, *args, **kwargs):
        """
        Needs an extra parameter `serializers` which has to be a dict
        key: value being `Model`: serializer.
        """
        super(GenericSerializerMixin, self).__init__(*args, **kwargs)
        self.serializers = serializers

    def to_internal_value(self, data):
        try:
            serializer = self.get_deserializer_for_data(data)
        except ImproperlyConfigured as e:
            raise serializers.ValidationError(e)
        return serializer

    def to_representation(self, instance):
        serializer = self.get_serializer_for_instance(instance)
        return serializer(instance=instance).data

    def get_serializer_for_instance(self, instance):
        for klass in instance.__class__.mro():
            if klass in self.serializers:
                return self.serializers[klass]

        raise serializers.ValidationError(self.error_messages['no_model_match'])

    def get_deserializer_for_data(self, value):
        tip = value.pop("tip")
        serializer = self.serializers[tip]
        serializer = serializer(data=value)
        serializer.is_valid(raise_exception=True)
        return serializer
