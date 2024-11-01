from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import auth_views

schema_view = get_schema_view(
   openapi.Info(
      title="Campus Connect API",
      default_version='v1',
      description="API documentation for the Campus Connect System",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication endpoints
    path('api/auth/login/', auth_views.login_view, name='login'),
    path('api/auth/logout/', auth_views.logout_view, name='logout'),
    path('api/auth/refresh/', auth_views.refresh_token_view, name='refresh'),
    # App endpoints
    path('api/admin_system/', include('admin_system.urls')),
    path('api/student_interface/', include('student_interface.urls')),
    path('api/teacher_interface/', include('teacher_interface.urls')),
    path('api/placement_management/', include('placement_management.urls')),
    path('api/resource_person_management/', include('resource_person_management.urls')),
    path('api/common_features/', include('common_features.urls')),
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
