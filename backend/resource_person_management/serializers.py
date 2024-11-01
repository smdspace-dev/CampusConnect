from rest_framework import serializers
from .models import (
    ResourcePerson, Workshop, WorkshopRegistration, Consultation, 
    KnowledgeSharingPost, PostInteraction
)
from admin_system.models import Student

class ResourcePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourcePerson
        fields = '__all__'

class WorkshopSerializer(serializers.ModelSerializer):
    resource_person_name = serializers.CharField(source='resource_person.name', read_only=True)
    coordinator_name = serializers.CharField(source='coordinator.user.get_full_name', read_only=True)
    current_registrations = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()
    
    class Meta:
        model = Workshop
        fields = '__all__'
    
    def get_current_registrations(self, obj):
        return WorkshopRegistration.objects.filter(workshop=obj).count()
    
    def get_available_slots(self, obj):
        current = WorkshopRegistration.objects.filter(workshop=obj).count()
        return max(0, obj.max_participants - current)

class WorkshopRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    workshop_title = serializers.CharField(source='workshop.title', read_only=True)
    resource_person_name = serializers.CharField(source='workshop.resource_person.name', read_only=True)
    
    class Meta:
        model = WorkshopRegistration
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    resource_person_name = serializers.CharField(source='resource_person.name', read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'

class KnowledgeSharingPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()
    is_bookmarked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeSharingPost
        fields = '__all__'
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                student = Student.objects.get(user=request.user)
                return PostInteraction.objects.filter(
                    post=obj, 
                    student=student, 
                    interaction_type='like'
                ).exists()
            except Student.DoesNotExist:
                pass
        return False
    
    def get_is_bookmarked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                student = Student.objects.get(user=request.user)
                return PostInteraction.objects.filter(
                    post=obj, 
                    student=student, 
                    interaction_type='bookmark'
                ).exists()
            except Student.DoesNotExist:
                pass
        return False
