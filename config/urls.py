from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from applications.utils.auth_views import CustomTokenObtainPairView, ValidateTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/auth/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', ValidateTokenView.as_view(), name='token_verify'),

    # module users
    path('api/users/', include('applications.users.urls')),

    # module inspections
    path('api/inspections/', include('applications.inspections.urls')),

    # module observations
    path('api/observations/', include('applications.observations.urls')),

    # routes for fcm_django
    path('', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
