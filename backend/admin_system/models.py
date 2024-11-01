import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('project', 'Project'),
        ('seminar', 'Seminar'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='theory')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['semester', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"

class Staff(models.Model):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('placement_officer', 'Placement Officer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='teacher')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date_of_joining = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    password_reset_token = models.CharField(max_length=128, blank=True)
    toggle_access = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def toggle(self):
        self.toggle_access = not self.toggle_access
        self.save()
        return self.toggle_access

    def generate_reset_token(self):
        token = uuid.uuid4().hex
        self.password_reset_token = token
        self.save()
        return token

class Cluster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='clusters')
    mentor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_clusters')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.department.code}"

class Club(models.Model):
    CLUB_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('literary', 'Literary'),
        ('social_service', 'Social Service'),
        ('hobby', 'Hobby'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    club_type = models.CharField(max_length=20, choices=CLUB_TYPE_CHOICES, default='technical')
    coordinator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='coordinated_clubs')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='clubs')
    members = models.ManyToManyField('Student', blank=True, related_name='clubs')
    max_members = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=1)
    phone = models.CharField(max_length=15, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year', 'roll_number']

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name() or self.user.username}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    grade = models.CharField(max_length=2, blank=True)  # A+, A, B+, B, etc.
    marks = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    enrolled_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['student', 'course', 'semester', 'academic_year']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code} ({self.academic_year})"
