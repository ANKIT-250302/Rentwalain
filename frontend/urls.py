from django.urls import path
from frontend.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/<int:id>/',ProfileView.as_view(),name='addProfile'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/addProperty/',AddPropertyView.as_view(),name='addProperty'),
    path('profile/view/<int:id>/',ViewEditProperty.as_view(),name='viewProperty'),
    path('profile/delete/<int:id>/',DeleteProperty.as_view(),name='deleteProperty'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)