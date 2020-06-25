from rest_framework import serializers
from ..models.keydoc import KeyDoc

class KeyDocSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = KeyDoc
        fields = ['creator', 'date_created', 'members_when_created']
