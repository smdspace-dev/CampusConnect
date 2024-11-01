from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Course, Staff, Cluster, Club, Student, Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DepartmentSerializer(serializers.ModelSerializer):
    head_of_department_name = serializers.CharField(source='head_of_department.get_full_name', read_only=True)
    total_staff = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
    
    def get_total_staff(self, obj):
        return Staff.objects.filter(department=obj, is_active=True).count()
    
    def get_total_students(self, obj):
        return Student.objects.filter(department=obj, is_active=True).count()

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    # Write-only fields for creation/updates
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Staff
        fields = '__all__'

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', 'defaultpass123')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        email = validated_data.pop('email', '')
        
        if username:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            validated_data['user'] = user
        
        staff = Staff.objects.create(**validated_data)
        return staff
    
    def update(self, instance, validated_data):
        # Handle user updates if provided
        user_fields = ['username', 'first_name', 'last_name', 'email']
        user_data = {}
        for field in user_fields:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        if user_data and instance.user:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()
        
        # Handle password update
        password = validated_data.pop('password', None)
        if password and instance.user:
            instance.user.set_password(password)
            instance.user.save()
        
        # Update staff fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        return instance

class ClusterSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source='mentor.user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Cluster
        fields = '__all__'
    
    def get_total_students(self, obj):
        return Student.objects.filter(cluster=obj, is_active=True).count()

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    cluster_name = serializers.CharField(source='cluster.name', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    # Write-only fields for creation/updates
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', 'defaultpass123')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        email = validated_data.pop('email', '')
        
        if username:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            validated_data['user'] = user
        
        student = Student.objects.create(**validated_data)
        return student
    
    def update(self, instance, validated_data):
        # Handle user updates if provided
        user_fields = ['username', 'first_name', 'last_name', 'email']
        user_data = {}
        for field in user_fields:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        if user_data and instance.user:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()
        
        # Handle password update
        password = validated_data.pop('password', None)
        if password and instance.user:
            instance.user.set_password(password)
            instance.user.save()
        
        # Update student fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        return instance

class ClubSerializer(serializers.ModelSerializer):
    coordinator_name = serializers.CharField(source='coordinator.user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    current_members = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = '__all__'
    
    def get_current_members(self, obj):
        from student_interface.models import ClubMembership
        return ClubMembership.objects.filter(club=obj, is_active=True).count()
    
    def get_available_slots(self, obj):
        from student_interface.models import ClubMembership
        current = ClubMembership.objects.filter(club=obj, is_active=True).count()
        return max(0, obj.max_members - current)

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
