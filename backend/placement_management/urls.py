from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, JobPostingViewSet, StudentApplicationViewSet,
    PlacementRecordViewSet, TrainingProgramViewSet, TrainingEnrollmentViewSet,
    InterviewScheduleViewSet, placement_dashboard_stats
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'job-postings', JobPostingViewSet, basename='job-postings')
router.register(r'applications', StudentApplicationViewSet, basename='student-applications')
router.register(r'placements', PlacementRecordViewSet, basename='placement-records')
router.register(r'training-programs', TrainingProgramViewSet, basename='training-programs')
router.register(r'training-enrollments', TrainingEnrollmentViewSet, basename='training-enrollments')
router.register(r'interviews', InterviewScheduleViewSet, basename='interview-schedules')

urlpatterns = [
    path('dashboard/stats/', placement_dashboard_stats, name='placement-dashboard-stats'),
    path('', include(router.urls)),
]
