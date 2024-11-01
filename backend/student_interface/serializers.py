from rest_framework import serializers
from .models import StudentProfile, ClubMembership, Grade, StudentFeedback, StudentAchievement
from admin_system.models import Student, Club, Course, Department
from teacher_interface.models import Assignment, AssignmentSubmission, Attendance
from common_features.models import Event
from django.contrib.auth.models import User

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class StudentProfileSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
    
    def get_student_details(self, obj):
        return {
            'roll_number': obj.student.roll_number,
            'user': UserSimpleSerializer(obj.student.user).data,
            'department': obj.student.department.name if obj.student.department else None,
            'year': obj.student.year,
            'semester': obj.student.semester
        }

class ClubMembershipSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = ClubMembership
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = Grade
        fields = '__all__'

class StudentFeedbackSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = StudentFeedback
        fields = '__all__'

class StudentAchievementSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = StudentAchievement
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course_assignment.course.name', read_only=True)
    teacher_name = serializers.CharField(source='course_assignment.teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course_assignment.course.name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'

class StudentDashboardSerializer(serializers.Serializer):
    student_info = StudentProfileSerializer(read_only=True)
    recent_grades = GradeSerializer(many=True, read_only=True)
    upcoming_assignments = AssignmentSerializer(many=True, read_only=True)
    recent_attendance = AttendanceSerializer(many=True, read_only=True)
    club_memberships = ClubMembershipSerializer(many=True, read_only=True)
    achievements = StudentAchievementSerializer(many=True, read_only=True)
    upcoming_events = serializers.ListField(child=serializers.CharField(), read_only=True)
