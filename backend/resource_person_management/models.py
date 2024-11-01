from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_system.models import Department, Student, Staff

class ResourcePerson(models.Model):
    PERSON_TYPE_CHOICES = [
        ('industry_expert', 'Industry Expert'),
        ('alumnus', 'Alumnus'),
        ('guest_faculty', 'Guest Faculty'),
        ('consultant', 'Consultant'),
        ('entrepreneur', 'Entrepreneur'),
        ('researcher', 'Researcher'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    person_type = models.CharField(max_length=20, choices=PERSON_TYPE_CHOICES, default='industry_expert')
    organization = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    expertise_areas = models.TextField()  # Comma-separated areas
    bio = models.TextField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    preferred_contact_method = models.CharField(max_length=20, default='email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_sessions = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.organization}"

class Workshop(models.Model):
    WORKSHOP_TYPE_CHOICES = [
        ('technical', 'Technical Workshop'),
        ('soft_skills', 'Soft Skills'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('career_guidance', 'Career Guidance'),
        ('industry_trends', 'Industry Trends'),
        ('research', 'Research Methodology'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    workshop_type = models.CharField(max_length=20, choices=WORKSHOP_TYPE_CHOICES, default='technical')
    resource_person = models.ForeignKey(ResourcePerson, on_delete=models.CASCADE, related_name='workshops')
    target_departments = models.ManyToManyField(Department, blank=True, related_name='workshops')
    target_years = models.CharField(max_length=50, default='1,2,3,4')  # Comma-separated years
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    max_participants = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    registration_deadline = models.DateTimeField()
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    certificate_provided = models.BooleanField(default=True)
    materials_provided = models.BooleanField(default=False)
    prerequisites = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    coordinator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='coordinated_workshops')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.resource_person.name}"

class WorkshopRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='workshop_registrations')
    registered_at = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, default='pending')
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    feedback_rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback_comments = models.TextField(blank=True)
    certificate_issued = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    
    class Meta:
        unique_together = ['workshop', 'student']

    def __str__(self):
        return f"{self.student.roll_number} - {self.workshop.title}"

class Consultation(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ('career_guidance', 'Career Guidance'),
        ('project_mentoring', 'Project Mentoring'),
        ('research_guidance', 'Research Guidance'),
        ('entrepreneurship', 'Entrepreneurship Guidance'),
        ('technical_help', 'Technical Help'),
    ]
    
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='consultations')
    resource_person = models.ForeignKey(ResourcePerson, on_delete=models.CASCADE, related_name='consultations')
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPE_CHOICES, default='career_guidance')
    topic = models.CharField(max_length=200)
    description = models.TextField()
    preferred_date = models.DateTimeField()
    actual_date = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=60, validators=[MinValueValidator(15), MaxValueValidator(180)])
    mode = models.CharField(max_length=20, default='online')  # online, offline
    meeting_link = models.URLField(blank=True)
    venue = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    notes = models.TextField(blank=True)
    student_feedback = models.TextField(blank=True)
    resource_person_feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.roll_number} - {self.resource_person.name} - {self.topic}"

class KnowledgeSharingPost(models.Model):
    POST_TYPE_CHOICES = [
        ('article', 'Article'),
        ('tutorial', 'Tutorial'),
        ('case_study', 'Case Study'),
        ('industry_update', 'Industry Update'),
        ('research_paper', 'Research Paper'),
        ('best_practice', 'Best Practice'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=250)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='article')
    author = models.ForeignKey(ResourcePerson, on_delete=models.CASCADE, related_name='posts')
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    featured_image = models.CharField(max_length=500, blank=True)
    attachments = models.TextField(blank=True)  # JSON field for file paths
    target_audience = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(max_length=20, default='intermediate')
    estimated_read_time = models.IntegerField(default=5)  # In minutes
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.name}"

class PostInteraction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('like', 'Like'),
        ('bookmark', 'Bookmark'),
        ('share', 'Share'),
    ]
    
    post = models.ForeignKey(KnowledgeSharingPost, on_delete=models.CASCADE, related_name='interactions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='post_interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['post', 'student', 'interaction_type']

    def __str__(self):
        return f"{self.student.roll_number} - {self.interaction_type} - {self.post.title}"
