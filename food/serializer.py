from rest_framework import serializers

from .models import FoodMenu


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodMenu
        fields = ("year", "month", "day", "breakfast", "lunch", "dinner")
        read_only_fields = ("year", "month", "day", "breakfast", "lunch", "dinner")
