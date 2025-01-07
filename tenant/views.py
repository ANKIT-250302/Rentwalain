import jwt # type: ignore 
from .models import TenantProfile
from rest_framework import status
from rest_framework import filters
from .filters import PropertyFilter
from properties.models import *
from properties.serializers import *
from Rentwalain.settings import SECRET_KEY
from rest_framework.response import Response
from tenant.authentication import Authentication,IsTenant
from rest_framework.viewsets import ModelViewSet 
from django.contrib.auth.hashers import check_password
from tenant.serializers import *
from django_filters.rest_framework import DjangoFilterBackend # type: ignore

class ProfileRegisterViews(ModelViewSet):
    serializer_class = ProfileSerializer
    http_method_names = ['post']
    
class ProfileAuthViews(ModelViewSet):
    serializer_class= ProfileAuthSerializer
    http_method_names = ['post']
    
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            data = TenantProfile.objects.filter(email=email).first()
            if data:
                if check_password(password, data.password):
                    encoded = jwt.encode({"id": data.id,'email':email,'type':'T'}, SECRET_KEY, algorithm="HS256")
                    return Response({'token':encoded}, status=status.HTTP_200_OK)
                else:   
                    return Response({'password': 'password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)  
            else:
                return Response({'email': 'no user found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'email and password both are required'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileMeViews(ModelViewSet):
    permission_classes = [IsTenant]
    serializer_class = ProfileMeSerializer
    http_method_names = ['get','patch']
    
    def list(self, request, *args, **kwargs):
        user = Authentication(request)
        profile = TenantProfile.objects.filter(id = user.get('id')).first()
        profile = ProfileMeSerializer(profile)
        return Response(profile.data)


class TenantPropertyViewSet(ModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = {
        'list': PropertyGetSerializer,
        'retrieve': PropertyViewSerializer,
    }
    default_serializer = PropertyGetSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['city']
    filterset_class = PropertyFilter
    http_method_names = ['get']
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer)
