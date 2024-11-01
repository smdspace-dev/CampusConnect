from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseAssignmentViewSet, ClassScheduleViewSet,
    AssignmentViewSet, CounselingSessionViewSet,
    teacher_dashboard_stats, attendance_list, mark_attendance, 
    class_attendance, student_performance
)

router = DefaultRouter()
router.register(r'course-assignments', CourseAssignmentViewSet, basename='course-assignments')
router.register(r'class-schedules', ClassScheduleViewSet, basename='class-schedules')
router.register(r'assignments', AssignmentViewSet, basename='teacher-assignments')
router.register(r'counseling', CounselingSessionViewSet, basename='counseling-sessions')

urlpatterns = [
    path('dashboard/stats/', teacher_dashboard_stats, name='teacher-dashboard-stats'),
    path('attendance/', attendance_list, name='attendance-list'),
    path('attendance/mark_attendance/', mark_attendance, name='mark-attendance'),
    path('attendance/class_attendance/', class_attendance, name='class-attendance'),
    path('student-performance/', student_performance, name='student-performance'),
    path('', include(router.urls)),
]
