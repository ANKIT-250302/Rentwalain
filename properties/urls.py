from django.urls import path, include
from rest_framework.routers import DefaultRouter
from properties.views import *
router = DefaultRouter()
router.register('rentals', PropertyViewSet, basename='property')
router.register('propertytype', PropertyTypeViewSet, basename='propertytype')
router.register('propertyImages', PropertyImageViewSet, basename='propertyimages')


urlpatterns = router.urls + [
]