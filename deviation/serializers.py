from rest_framework import serializers


class StandardDeviationSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.DictField()
