from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('parking.urls')),
]

urlpatterns += doc_urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
