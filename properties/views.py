from rest_framework.viewsets import ModelViewSet
from landlord.authentication import IsLandlord
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache



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
    
    
    def retrieve(self, request, *args, **kwargs):
        property_id = kwargs.get('pk')
        cache_key = f"property_{property_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            # print(".......Cache.......")
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        cache.set(cache_key, data, timeout=60 * 15)
        # print(".......DB.......")
        return Response(data)
    
    def partial_update(self, request, *args, **kwargs):
        property_id = kwargs.get('pk')
        cache_key = f"property_{property_id}"
        cache.delete(cache_key)
        return super().partial_update(request, *args, **kwargs)

    
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

class ApplicationViewSet(ModelViewSet):
    permission_classes = [IsLandlord]
    serializer_class = ApplicationSerializer
    
    def get_queryset(self):
        applicants = Application.objects.filter(property__landlord_id=self.request.user_id)
        return applicants
    
    
    
    
    
    
    
    
    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     tenant = TenantProfile.objects.get(user=user)
    #     if not tenant:
    #         return Response({"error": "Tenant profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    #     property_id = request.data.get('property')
    #     property_obj = Property.objects.get(id=property_id)
    #     if not property_obj:
    #         return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)
        
    #     # Check for duplicate application
    #     if Application.objects.filter(tenant=tenant, property=property_obj).exists():
    #         return Response({"error": "You have already applied for this property."}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create application
    #     application = Application.objects.create(tenant=tenant, property=property_obj)
    #     serializer = self.get_serializer(application)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    

        
    