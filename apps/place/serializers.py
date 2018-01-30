from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    
    # Atribut ini akan dikalkukasi 'On-the-fly' untuk memberi informasi
    # bahwa place sudah di beri rate oleh user atau belum
    is_rated = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = '__all__'
        
    def get_owner(self, obj):
        return obj.owner.username
    
    def get_picture(self, obj):
        return obj.get_picture_url
    
    def get_is_rated(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated() :
            if obj.userrate_set.filter(user=user):
                return True
            else :
                return False
        else :
            return False
        

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
          write_only=True,
    )

    class Meta:
       model = User
       fields = ('password', 'username', 'first_name', 'last_name',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
              user.set_password(validated_data['password'])
              user.save()
        return user