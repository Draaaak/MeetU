from rest_framework.serializers import Field
from meetYou.serializers import GenericSerializerMixin


class GenericRelatedField(GenericSerializerMixin, Field):
    """
    Represents a generic relation / foreign key.
    It's actually more of a wrapper, that delegates the logic to registered
    serializers based on the `Model` class.
    """
