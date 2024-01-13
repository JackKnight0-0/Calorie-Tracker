from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('profile/', include('userprofile.urls')),
    path('calorie/', include('calorie_tracker.urls')),
    path('', include('pages.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
