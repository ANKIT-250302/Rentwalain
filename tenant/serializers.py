from rest_framework import serializers
from tenant.models import TenantProfile
from django.contrib.auth.hashers import make_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'password','profilepic']

    def create(self, validated_data):
        validated_data['password']  = make_password(validated_data['password'])
        return super().create(validated_data)

class ProfileAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ['email', 'password']
        
class ProfileMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number','is_active','profilepic']
