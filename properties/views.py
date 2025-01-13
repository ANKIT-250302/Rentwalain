from rest_framework.viewsets import ModelViewSet
from landlord.authentication import IsLandlord
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PropertyTypeViewSet(ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

class PropertyViewSet(ModelViewSet):
    http_method_names  = ['get','post','patch','delete']
    permission_classes = [IsLandlord]
    serializer_class = {
        'create' : PropertySerializer,
        'list' : PropertyGetSerializer,
        'retrieve' : PropertyViewSerializer,
    }
    default_serializer = PropertySerializer
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer)
    
    def get_queryset(self):
        return Property.objects.filter(landlord_id=self.request.user_id).order_by('-created_at')
    
    def get_serializer_context(self):
        return {'user_is':self.request.user_id,}
    
class PropertyImageViewSet(ModelViewSet):
    http_method_names  = ['get','post','patch','delete']
    permission_classes = [IsLandlord]
    serializer_class = PropertyImageSerializer
    def get_queryset(self):
        properties = Property.objects.filter(landlord_id=self.request.user_id)
        images = PropertyImage.objects.filter(property__in=properties)
        return images
    
    def get_serializer_context(self):
        return {'user_is':self.request.user_id}


    
    
    

        
    