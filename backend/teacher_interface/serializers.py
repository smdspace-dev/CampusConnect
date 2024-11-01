from rest_framework import serializers
from .models import (
    TeacherProfile, CourseAssignment, ClassSchedule, Assignment, 
    AssignmentSubmission, Attendance, CounselingSession
)
from admin_system.models import Staff, Student, Course

class TeacherProfileSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='staff.department.name', read_only=True)
    
    class Meta:
        model = TeacherProfile
        fields = '__all__'

class CourseAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = CourseAssignment
        fields = '__all__'

class ClassScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course_assignment.course.name', read_only=True)
    teacher_name = serializers.CharField(source='course_assignment.teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course_assignment.course.name', read_only=True)
    course_code = serializers.CharField(source='course_assignment.course.code', read_only=True)
    teacher_name = serializers.CharField(source='course_assignment.teacher.user.get_full_name', read_only=True)
    total_submissions = serializers.SerializerMethodField()
    graded_submissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = '__all__'
    
    def get_total_submissions(self, obj):
        return AssignmentSubmission.objects.filter(assignment=obj).count()
    
    def get_graded_submissions(self, obj):
        return AssignmentSubmission.objects.filter(assignment=obj, status='graded').count()

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    max_marks = serializers.CharField(source='assignment.max_marks', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    course_name = serializers.CharField(source='course_assignment.course.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'

class CounselingSessionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = CounselingSession
        fields = '__all__'
