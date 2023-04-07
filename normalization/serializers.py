from rest_framework import serializers


class StandardizationSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.DictField()
