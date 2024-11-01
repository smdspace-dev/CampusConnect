from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_system.models import Cluster, Staff, Student, Club, Course
from teacher_interface.models import Assignment

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    hobbies = models.CharField(max_length=200, blank=True)
    career_goals = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.get_full_name() or self.student.user.username} Profile"

class ClubMembership(models.Model):
    POSITION_CHOICES = [
        ('member', 'Member'),
        ('secretary', 'Secretary'),
        ('vice_president', 'Vice President'),
        ('president', 'President'),
        ('coordinator', 'Coordinator'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='club_memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='member')
    joined_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    achievements = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'club']

    def __str__(self):
        return f"{self.student.roll_number} - {self.club.name} ({self.position})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    internal_marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)], default=0)
    external_marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], default=0)
    total_marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    grade = models.CharField(max_length=2, blank=True)  # A+, A, B+, B, C, etc.
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=100, blank=True)
    is_passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']
    
    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks
        # Calculate grade based on total marks
        if self.total_marks >= 90:
            self.grade = 'A+'
            self.gpa = 10.0
        elif self.total_marks >= 80:
            self.grade = 'A'
            self.gpa = 9.0
        elif self.total_marks >= 70:
            self.grade = 'B+'
            self.gpa = 8.0
        elif self.total_marks >= 60:
            self.grade = 'B'
            self.gpa = 7.0
        elif self.total_marks >= 50:
            self.grade = 'C'
            self.gpa = 6.0
        elif self.total_marks >= 40:
            self.grade = 'D'
            self.gpa = 5.0
        else:
            self.grade = 'F'
            self.gpa = 0.0
        
        self.is_passed = self.total_marks >= 40
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} - {self.grade}"

class StudentFeedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('course', 'Course Feedback'),
        ('teacher', 'Teacher Feedback'),
        ('facility', 'Facility Feedback'),
        ('general', 'General Feedback'),
    ]
    
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='general')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField()
    suggestions = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Feedback by {self.student.roll_number} - {self.feedback_type} ({self.rating}/5)"

class StudentAchievement(models.Model):
    ACHIEVEMENT_TYPE_CHOICES = [
        ('academic', 'Academic Achievement'),
        ('sports', 'Sports Achievement'),
        ('cultural', 'Cultural Achievement'),
        ('technical', 'Technical Achievement'),
        ('leadership', 'Leadership Achievement'),
        ('social_service', 'Social Service'),
        ('competition', 'Competition'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES, default='academic')
    date_achieved = models.DateField()
    certificate_file = models.CharField(max_length=500, blank=True)  # For file uploads
    verified_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_achievements')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_achieved']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.title}"
