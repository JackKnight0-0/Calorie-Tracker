from django.urls import path, include, re_path
from .views import CustomSingUpView, CustomLoginView, CustomPasswordChangeView, CustomPasswordResetView, \
    CustomPasswordResetFromKeyView

urlpatterns = [
    path('signup/', CustomSingUpView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", CustomPasswordResetFromKeyView.as_view(),
            name='account_reset_password_from_key'),
    path('', include('allauth.account.urls'))
]
