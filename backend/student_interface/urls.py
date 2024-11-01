from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardView, StudentProfileViewSet, ClubViewSet, GradeViewSet,
    AttendanceViewSet, AssignmentViewSet, AchievementViewSet,
    StudentCourseViewSet, StudentAssignmentViewSet, StudentGradeViewSet,
    student_dashboard_stats
)

router = DefaultRouter()
router.register(r'profile', StudentProfileViewSet, basename='student-profile')
router.register(r'clubs', ClubViewSet, basename='student-clubs')
router.register(r'grades', GradeViewSet, basename='student-grades')
router.register(r'attendance', AttendanceViewSet, basename='student-attendance')
router.register(r'assignments', AssignmentViewSet, basename='student-assignments')
router.register(r'achievements', AchievementViewSet, basename='student-achievements')
router.register(r'courses', StudentCourseViewSet, basename='student-courses')
router.register(r'my-assignments', StudentAssignmentViewSet, basename='student-my-assignments')
router.register(r'my-grades', StudentGradeViewSet, basename='student-my-grades')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='student-dashboard'),
    path('dashboard/stats/', student_dashboard_stats, name='student-dashboard-stats'),
    path('', include(router.urls)),
]
