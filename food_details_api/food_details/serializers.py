from rest_framework import serializers
from .models import FoodTable


class FoodTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTable
        fields = "__all__"


class APIInfoSerializer(serializers.Serializer):
    db_connection = serializers.BooleanField()
    last_cron_exec = serializers.DateTimeField()
    running_time = serializers.CharField()
    memory_usage = serializers.CharField()
