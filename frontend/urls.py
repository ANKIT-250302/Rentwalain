from django.urls import path
from frontend.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('details/<int:id>/',DetailsView.as_view(),name='details'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/<int:id>/',ProfileView.as_view(),name='addProfile'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/addProperty/',AddPropertyView.as_view(),name='addProperty'),
    path('profile/image/add/<int:id>',EditImageView.as_view(),name='addImage'),
    path('profile/view/<int:id>/',ViewEditProperty.as_view(),name='viewProperty'),
    path('profile/delete/<int:id>/',DeleteProperty.as_view(),name='deleteProperty'),
    path('profile/image/delete/<int:id>/',EditImageView.as_view(),name='deleteImage'),
    path("apply/<int:id>/", ApplyForProperty.as_view(), name="applyForProperty"),
    path("applicants/", ApplicantView.as_view(), name="applicants"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)