from django.urls import path, include
from rest_framework.routers import DefaultRouter
from properties.views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('rentals', PropertyViewSet, basename='property')
router.register('propertytype', PropertyTypeViewSet, basename='propertytype')
router.register('propertyImages', PropertyImageViewSet, basename='propertyimages')
router.register(r'applications', ApplicationViewSet, basename='application')


urlpatterns = router.urls + [
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)