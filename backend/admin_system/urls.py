from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, CourseViewSet, StaffViewSet, ClusterViewSet,
    StudentViewSet, ClubViewSet, EnrollmentViewSet, StudentBulkUploadView,
    admin_dashboard_stats, academic_overview
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'clusters', ClusterViewSet, basename='clusters')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    path('dashboard/stats/', admin_dashboard_stats, name='admin-dashboard-stats'),
    path('academic/overview/', academic_overview, name='academic-overview'),
    path('students/bulk-upload/', StudentBulkUploadView.as_view(), name='student-bulk-upload'),
    path('', include(router.urls)),
]
