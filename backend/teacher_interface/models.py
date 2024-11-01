from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_system.models import Department, Cluster, Student, Staff, Course

class TeacherProfile(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='teacher_profile')
    specialization = models.CharField(max_length=200, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    research_interests = models.TextField(blank=True)
    publications = models.TextField(blank=True)
    is_available_for_counseling = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prof. {self.staff.user.get_full_name() or self.staff.user.username}"

class CourseAssignment(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='course_assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['teacher', 'course', 'semester', 'academic_year']
    
    def __str__(self):
        return f"{self.teacher.user.username} - {self.course.code} ({self.academic_year})"

class ClassSchedule(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    
    course_assignment = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.course_assignment.course.code} - {self.day_of_week} {self.start_time}"

class Assignment(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('lab', 'Lab Assignment'),
        ('quiz', 'Quiz'),
        ('presentation', 'Presentation'),
    ]
    
    course_assignment = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES, default='homework')
    due_date = models.DateTimeField()
    max_marks = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course_assignment.course.code} - {self.title}"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late Submission'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_text = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)  # For file uploads
    marks_obtained = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.assignment.title}"

class Attendance(models.Model):
    course_assignment = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.CharField(max_length=100, blank=True)
    marked_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='marked_attendances')
    marked_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['course_assignment', 'student', 'date']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.roll_number} - {self.course_assignment.course.code} - {self.date} ({status})"

class CounselingSession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('academic', 'Academic Counseling'),
        ('career', 'Career Guidance'),
        ('personal', 'Personal Counseling'),
        ('disciplinary', 'Disciplinary'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='counseling_sessions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='counseling_sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='academic')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(15), MaxValueValidator(120)])
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.teacher.user.username} - {self.student.roll_number} ({self.scheduled_date})"
