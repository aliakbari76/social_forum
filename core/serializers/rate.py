from rest_framework import serializers


class RateSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    rate = serializers.IntegerField()

