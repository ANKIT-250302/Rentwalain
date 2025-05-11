from django.urls import path,include
from rest_framework.routers import DefaultRouter
from tenant.views import *
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register('register', ProfileRegisterViews, basename='tenant_register')
router.register('login',ProfileAuthViews, basename='tenant_login')
router.register('profile',ProfileMeViews,basename='tenant_profile')
router.register('home',TenantPropertyViewSet,basename='home')
router.register("apply",ApplicantView,basename="apply_rent")

urlpatterns = router.urls + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + [
]
