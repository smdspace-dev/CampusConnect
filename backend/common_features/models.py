from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_system.models import Department, Student, Staff

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('technical', 'Technical'),
        ('sports', 'Sports'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('competition', 'Competition'),
        ('placement', 'Placement'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=250)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='academic')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    organizer = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='organized_events')
    target_departments = models.ManyToManyField(Department, blank=True, related_name='events')
    max_participants = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    registration_required = models.BooleanField(default=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    poster_image = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.start_date.date()}"

class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, default='pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    feedback_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback_comments = models.TextField(blank=True)
    certificate_issued = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['event', 'student']

    def __str__(self):
        return f"{self.student.roll_number} - {self.event.title}"

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('reminder', 'Reminder'),
        ('announcement', 'Announcement'),
    ]
    
    RECIPIENT_TYPE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('all', 'All Users'),
        ('department', 'Department'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default='info')
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES, default='all')
    sender = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='sent_notifications')
    target_departments = models.ManyToManyField(Department, blank=True, related_name='notifications')
    target_users = models.ManyToManyField(User, blank=True, related_name='targeted_notifications')
    is_global = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.notification_type}"

class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_reads')
    read_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['notification', 'user']

    def __str__(self):
        return f"{self.user.username} read {self.notification.title}"

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('attendance', 'Attendance Report'),
        ('academic', 'Academic Performance'),
        ('placement', 'Placement Statistics'),
        ('financial', 'Financial Report'),
        ('event', 'Event Report'),
        ('custom', 'Custom Report'),
    ]
    
    STATUS_CHOICES = [
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='custom')
    generated_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='generated_reports')
    parameters = models.JSONField(default=dict, blank=True)  # Report parameters
    data = models.JSONField(default=dict, blank=True)  # Report data
    file_path = models.CharField(max_length=500, blank=True)  # Path to generated file
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generating')
    generated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.generated_by.user.username}"

class SystemConfiguration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    changes = models.JSONField(default=dict, blank=True)  # What changed
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown'} - {self.action} - {self.model_name}"

class GoogleClassroomIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classroom_integrations')
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Google Classroom"
    created_at = models.DateTimeField(default=timezone.now)
