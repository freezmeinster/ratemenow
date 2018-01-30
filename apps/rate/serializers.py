from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRate

class UserRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRate
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
