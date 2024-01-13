from django.urls import path
from .views import UserProfileView, ChangeUserProfile

urlpatterns = [
    path('change/', ChangeUserProfile.as_view(), name='change_profile'),
    path('<slug:slug>/', UserProfileView.as_view(), name='profile'),
]
