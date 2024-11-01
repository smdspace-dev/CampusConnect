from rest_framework import serializers
from .models import Event, EventRegistration, Notification, Report, SystemConfiguration, AuditLog
from admin_system.models import Student, Staff

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.get_full_name', read_only=True)
    registrations_count = serializers.IntegerField(read_only=True)
    available_slots = serializers.SerializerMethodField()
    is_registration_open = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
    
    def get_available_slots(self, obj):
        if obj.max_participants:
            return obj.max_participants - obj.registrations.count()
        return None
    
    def get_is_registration_open(self, obj):
        from django.utils import timezone
        return (obj.registration_deadline and 
                obj.registration_deadline > timezone.now() and
                obj.status == 'upcoming')

class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    event_date = serializers.DateTimeField(source='event.date_time', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.SerializerMethodField()
    is_read = serializers.BooleanField(read_only=True)
    time_since = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = '__all__'
    
    def get_recipient_name(self, obj):
        if obj.recipient_student:
            return obj.recipient_student.get_full_name()
        elif obj.recipient_staff:
            return obj.recipient_staff.get_full_name()
        return "All Users"
    
    def get_time_since(self, obj):
        from django.utils import timezone
        from django.utils.timesince import timesince
        return timesince(obj.created_at, timezone.now())

class ReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    file_size = serializers.SerializerMethodField()
    is_downloadable = serializers.SerializerMethodField()
    
    class Meta:
        model = Report
        fields = '__all__'
    
    def get_file_size(self, obj):
        if obj.file_path and hasattr(obj.file_path, 'size'):
            return obj.file_path.size
        return None
    
    def get_is_downloadable(self, obj):
        return obj.status == 'completed' and obj.file_path

class SystemConfigurationSerializer(serializers.ModelSerializer):
    updated_by_name = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = SystemConfiguration
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    formatted_timestamp = serializers.DateTimeField(source='timestamp', format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = '__all__'
    
    def get_user_name(self, obj):
        if obj.user_student:
            return obj.user_student.get_full_name()
        elif obj.user_staff:
            return obj.user_staff.get_full_name()
        return "System"
