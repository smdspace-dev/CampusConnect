from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from admin_system.models import Student, Staff, Department

class Company(models.Model):
    COMPANY_TYPE_CHOICES = [
        ('startup', 'Startup'),
        ('sme', 'Small & Medium Enterprise'),
        ('mnc', 'Multinational Corporation'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
    ]
    
    name = models.CharField(max_length=200)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, default='sme')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    hr_contact_name = models.CharField(max_length=100, blank=True)
    hr_contact_email = models.EmailField(blank=True)
    hr_contact_phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    eligible_departments = models.ManyToManyField(Department, blank=True, related_name='job_postings')
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=6.0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    max_backlogs = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    application_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company.name} - {self.title}"

class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('placed', 'Placed'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='job_applications')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    resume_file = models.CharField(max_length=500, blank=True)  # File path for resume
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)  # Internal notes by placement team
    
    class Meta:
        unique_together = ['student', 'job_posting']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.roll_number} - {self.job_posting.title} ({self.status})"

class InterviewSchedule(models.Model):
    INTERVIEW_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('hr', 'HR'),
        ('group_discussion', 'Group Discussion'),
        ('aptitude', 'Aptitude Test'),
        ('final', 'Final Interview'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    application = models.ForeignKey(StudentApplication, on_delete=models.CASCADE, related_name='interviews')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES, default='technical')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60, validators=[MinValueValidator(15), MaxValueValidator(300)])
    location = models.CharField(max_length=200, blank=True)
    interviewer_details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)
    result = models.CharField(max_length=20, blank=True)  # Pass/Fail/Pending
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.student.roll_number} - {self.interview_type} ({self.scheduled_date})"

class PlacementRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placements')
    job_title = models.CharField(max_length=200)
    package_offered = models.DecimalField(max_digits=10, decimal_places=2)  # Annual package
    joining_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    is_confirmed = models.BooleanField(default=False)
    offer_letter_file = models.CharField(max_length=500, blank=True)
    placed_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-placed_at']

    def __str__(self):
        return f"{self.student.roll_number} - {self.company.name} - {self.package_offered} LPA"

class TrainingProgram(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('aptitude', 'Aptitude Training'),
        ('technical', 'Technical Skills'),
        ('soft_skills', 'Soft Skills'),
        ('interview_prep', 'Interview Preparation'),
        ('resume_writing', 'Resume Writing'),
        ('group_discussion', 'Group Discussion'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES, default='technical')
    trainer_name = models.CharField(max_length=100)
    trainer_organization = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(500)])
    max_participants = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    venue = models.CharField(max_length=200, blank=True)
    is_mandatory = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

class TrainingEnrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]
    
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='training_enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    certificate_issued = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['program', 'student']

    def __str__(self):
        return f"{self.student.roll_number} - {self.program.title} ({self.status})"

class PlacementStatistics(models.Model):
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='placement_stats')
    total_students = models.IntegerField(default=0)
    placed_students = models.IntegerField(default=0)
    highest_package = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lowest_package = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_package = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    companies_visited = models.IntegerField(default=0)
    placement_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['academic_year', 'department']
        ordering = ['-academic_year', 'department']

    def __str__(self):
        return f"{self.department.code} - {self.academic_year} ({self.placement_percentage}%)"
