from rest_framework import serializers
from landlord.models import LandlordProfile
from django.contrib.auth.hashers import make_password
class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  
        return super().create(validated_data)
    
class ProfileAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = ['email', 'password']
        
class ProfileMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = "__all__"