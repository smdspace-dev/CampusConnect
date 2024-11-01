from rest_framework import routers
from django.urls import path, include
from .views import (
    EventViewSet, EventRegistrationViewSet, NotificationViewSet,
    ReportViewSet, SystemConfigurationViewSet, AuditLogViewSet,
    event_dashboard_stats
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='events')
router.register(r'event-registrations', EventRegistrationViewSet, basename='event-registrations')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'system-config', SystemConfigurationViewSet, basename='system-config')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = [
    path('events/dashboard/stats/', event_dashboard_stats, name='event-dashboard-stats'),
    path('', include(router.urls)),
]
