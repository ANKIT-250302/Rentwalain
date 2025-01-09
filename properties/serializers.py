from rest_framework import serializers
from properties.models import *
from landlord.serializers import LandlordSerializer
from rest_framework.response import Response

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property','image']
    def validate_property(self, data):
        properties = Property.objects.filter(landlord_id = self.context.get('user_is'))
        owned_property_ids = properties.values_list('id', flat=True)
        if data.id not in owned_property_ids:
            raise serializers.ValidationError("You do not own this property.")
        return data

class PropertyGetSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer( many=True)
    class Meta:
        model = Property
        fields = ['id','title','description','price_per_month','images']

class PropertySerializer(serializers.ModelSerializer):
    landlord = serializers.CharField(read_only=True)
    images = serializers.ImageField(write_only = True)
    class Meta:
        model = Property
        fields = ['id','landlord','property_type','title','description','address','city','state','price_per_month','num_of_bedrooms','num_of_bathrooms','available_from','images']
        
    def create(self, validated_data):
        image_data = validated_data.pop('images', None)  # Extract images from the data
        validated_data['landlord_id'] = self.context.get('user_is')

        # Create the Property instance
        property_instance = super().create(validated_data)

        # Save the images associated with this property
        if image_data:
            PropertyImage.objects.create(property=property_instance, image=image_data)

        return property_instance
    


class PropertyViewSerializer(serializers.ModelSerializer):
    landlord = LandlordSerializer(read_only=True)
    images = PropertyImageSerializer( many=True)
    property_type= serializers.CharField()
    class Meta:
        model = Property
        fields = '__all__'


    
class PropertyTypeSerializer(serializers.ModelSerializer):
    landlord = serializers.CharField(read_only=True)
    class Meta:
        model = PropertyType
        fields = '__all__'

        
        