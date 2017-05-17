from rest_framework import serializers
from .models import UserRate

class UserRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRate
        fields = '__all__'