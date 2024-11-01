from rest_framework import serializers
from .models import (
    Company, JobPosting, StudentApplication, InterviewSchedule,
    PlacementRecord, TrainingProgram, TrainingEnrollment, PlacementStatistics
)
from admin_system.models import Student

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    eligible_departments_list = serializers.StringRelatedField(source='eligible_departments', many=True, read_only=True)
    
    class Meta:
        model = JobPosting
        fields = '__all__'

class StudentApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    job_title = serializers.CharField(source='job_posting.title', read_only=True)
    company_name = serializers.CharField(source='job_posting.company.name', read_only=True)
    
    class Meta:
        model = StudentApplication
        fields = '__all__'

class InterviewScheduleSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='application.student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='application.student.roll_number', read_only=True)
    company_name = serializers.CharField(source='application.job_posting.company.name', read_only=True)
    
    class Meta:
        model = InterviewSchedule
        fields = '__all__'

class PlacementRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = PlacementRecord
        fields = '__all__'

class TrainingProgramSerializer(serializers.ModelSerializer):
    current_enrollments = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainingProgram
        fields = '__all__'
    
    def get_current_enrollments(self, obj):
        return TrainingEnrollment.objects.filter(program=obj).count()
    
    def get_available_slots(self, obj):
        current = TrainingEnrollment.objects.filter(program=obj).count()
        return max(0, obj.max_participants - current)

class TrainingEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    program_title = serializers.CharField(source='program.title', read_only=True)
    
    class Meta:
        model = TrainingEnrollment
        fields = '__all__'

class PlacementStatisticsSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = PlacementStatistics
        fields = '__all__'
