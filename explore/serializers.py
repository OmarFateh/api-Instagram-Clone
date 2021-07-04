from explore.models import Hashtag 

from rest_framework import serializers


class HashtagSerializer(serializers.ModelSerializer):
    """
    Hashtag serializer.
    """
    id = serializers.IntegerField(required=False, write_only=False)

    class Meta:
        model  = Hashtag
        fields = ['id', 'name']

    def to_representation(self, value):
        return value.name