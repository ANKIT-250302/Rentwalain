from django.shortcuts import render
import jwt # type: ignore
from landlord.serializers import*
from rest_framework import status
from .models import LandlordProfile
from django.shortcuts import render
from rest_framework.views import APIView
from Rentwalain.settings import SECRET_KEY
from rest_framework.response import Response
from landlord.authentication import Authentication
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.hashers import check_password
    
class ProfileRegisterViews(ModelViewSet):
    serializer_class = LandlordSerializer
    http_method_names = ['post']
    
class ProfileAuthViews(ModelViewSet):
    serializer_class = ProfileAuthSerializer
    http_method_names = ['post']
    
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            data = LandlordProfile.objects.filter(email=email).first()
            if data:
                if check_password(password, data.password):
                    encoded = jwt.encode({"id": data.id,'email':email,'type':'L'}, SECRET_KEY, algorithm="HS256")
                    return Response({'token':encoded}, status=status.HTTP_200_OK)
                else:   
                    return Response({'password': 'password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)  
            else:
                return Response({'email': 'no user found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'email and password both are required'}, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileMeViews(ModelViewSet):
    serializer_class = ProfileMeSerializer
    http_method_names = ['get','patch']
    
    def list(self, request, *args, **kwargs):
        user = Authentication(request)
        id = user.get('id')
        data = LandlordProfile.objects.get(id= id)
        landlord = ProfileMeSerializer(data)
        return Response(landlord.data)
        # return Response(landlord.errors)
