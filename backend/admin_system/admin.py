from django.contrib import admin
from .models import Department, Course, Staff, Cluster, Student, Club, Enrollment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'credits', 'semester', 'is_active')
    list_filter = ('department', 'semester', 'is_active')
    search_fields = ('name', 'code')
    ordering = ('department', 'semester', 'name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'role', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__username',)

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'mentor', 'is_active', 'created_at')
    list_filter = ('department', 'is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('department', 'name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'year', 'semester', 'is_active')
    list_filter = ('department', 'year', 'semester', 'is_active', 'gender')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'roll_number')
    ordering = ('roll_number',)

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'club_type', 'department', 'coordinator', 'is_active', 'created_at')
    list_filter = ('club_type', 'department', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'academic_year', 'grade', 'is_active')
    list_filter = ('course__department', 'semester', 'academic_year', 'is_active')
    search_fields = ('student__roll_number', 'course__name', 'course__code')
    ordering = ('academic_year', 'semester', 'student__roll_number')
