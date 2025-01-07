from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('',include('frontend.urls')),
    path('property/', include('properties.urls')),
    path('landlord/', include('landlord.urls')),
    path('tenant/', include('tenant.urls')),
    path('admin/', admin.site.urls),
]
