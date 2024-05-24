from .views import *
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r"upload", UploadViewSet, basename="upload")

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include(router.urls)),
    path("import/", UploadAPIView.as_view(), name="import-api"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
