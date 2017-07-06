import sys, traceback
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Place
from .serializers import PlaceSerializer
from .serializers import UserSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rate.serializers import UserSerializer
from rate.serializers import UserRateSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token

# View Set ini untuk user registration
class CreateUserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.filter(is_active=True)
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        response= super(CreateUserViewSet, self).create(request, *args, **kwargs)
        user = User.objects.get(username=response.data.get("username"))
        token = Token.objects.create(user=user)
        return Response({ "token" : token.key })

# View set ini untuk place
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlaceSerializer
    
    @detail_route(methods=['post'])
    def rate(self,request,pk=None):
        response = {}
        if request.user.is_authenticated() :
            try :
                place = Place.objects.get(id=pk)
                data = request.data.copy()
                data['user'] = request.user.id
                data['place'] = pk
                rate = UserRateSerializer(data=data)
                if rate.is_valid():
                    rate.save()
                    response = { "status" : "success" ,"code" : 201, "message" : "Successfuly rated"}
                else :
                    response = { "status" : "error" ,"code" : 400, "message" : { "error" : rate.errors} }
            except :
                traceback.print_exc(file=sys.stdout)
                response = { "status" : "error" ,"code" : 404, "message" : "Place not found" }
        else :
            response = { "status" : "error" , "code" : 401, "message" : "Please authenticate first" }
        return Response(response, status=response.get("code"))