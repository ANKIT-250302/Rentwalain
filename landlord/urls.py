from django.urls import path, include
from rest_framework.routers import DefaultRouter
from landlord.views import *
router = DefaultRouter()
router.register('register', ProfileRegisterViews, basename='landlord_register')
router.register('login', ProfileAuthViews, basename='landlord_login')
router.register('profile', ProfileMeViews, basename='landlord_profile')

urlpatterns = router.urls + [
    
]