from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.utils import timezone

from .models import (
    Company, JobPosting, StudentApplication, InterviewSchedule,
    PlacementRecord, TrainingProgram, TrainingEnrollment, PlacementStatistics
)
from .serializers import (
    CompanySerializer, JobPostingSerializer, StudentApplicationSerializer,
    InterviewScheduleSerializer, PlacementRecordSerializer, 
    TrainingProgramSerializer, TrainingEnrollmentSerializer
)
from admin_system.models import Student

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def job_postings(self, request, pk=None):
        """Get job postings for a company"""
        company = self.get_object()
        postings = JobPosting.objects.filter(
            company=company, 
            is_active=True,
            application_deadline__gte=timezone.now()
        )
        serializer = JobPostingSerializer(postings, many=True)
        return Response(serializer.data)

class JobPostingViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = JobPosting.objects.filter(
            is_active=True,
            application_deadline__gte=timezone.now()
        )
        
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Sum, Max, Min
from django.utils import timezone
from datetime import timedelta

from .models import (
    Company, JobPosting, StudentApplication, InterviewSchedule,
    PlacementRecord, TrainingProgram, TrainingEnrollment, PlacementStatistics
)
from .serializers import (
    CompanySerializer, JobPostingSerializer, StudentApplicationSerializer,
    InterviewScheduleSerializer, PlacementRecordSerializer, 
    TrainingProgramSerializer, TrainingEnrollmentSerializer
)
from admin_system.models import Student, Staff

class IsPlacementOfficerRole(IsAuthenticated):
    """Custom permission class for placement officer access"""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        # Check if user has staff_profile with placement_officer role
        staff = getattr(request.user, 'staff_profile', None)
        if staff and staff.role in ('placement_officer', 'admin', 'super_admin'):
            return True
        return request.user.is_superuser

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsPlacementOfficerRole]
    
    def get_queryset(self):
        queryset = Company.objects.filter(is_active=True).order_by('name')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(industry__icontains=search) |
                Q(location__icontains=search)
            )
        
        # Filter by company type
        company_type = self.request.query_params.get('company_type', None)
        if company_type:
            queryset = queryset.filter(company_type=company_type)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def job_postings(self, request, pk=None):
        """Get job postings for a company"""
        company = self.get_object()
        postings = JobPosting.objects.filter(
            company=company, 
            is_active=True
        ).order_by('-created_at')
        
        serializer = JobPostingSerializer(postings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def placement_history(self, request, pk=None):
        """Get placement history for a company"""
        company = self.get_object()
        placements = PlacementRecord.objects.filter(
            company=company
        ).select_related('student__user').order_by('-placed_at')
        
        serializer = PlacementRecordSerializer(placements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get company statistics"""
        stats = {
            'total_companies': Company.objects.filter(is_active=True).count(),
            'companies_by_type': {},
            'active_job_postings': JobPosting.objects.filter(
                is_active=True,
                application_deadline__gte=timezone.now()
            ).count(),
            'top_recruiting_companies': Company.objects.filter(
                placements__isnull=False
            ).annotate(
                placement_count=Count('placements')
            ).order_by('-placement_count')[:5].values('name', 'placement_count')
        }
        
        # Companies by type
        for company_type_choice in Company.COMPANY_TYPE_CHOICES:
            type_code = company_type_choice[0]
            count = Company.objects.filter(
                company_type=type_code, 
                is_active=True
            ).count()
            stats['companies_by_type'][company_type_choice[1]] = count
        
        return Response(stats)

class JobPostingViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostingSerializer
    permission_classes = [IsPlacementOfficerRole]
    
    def get_queryset(self):
        queryset = JobPosting.objects.filter(is_active=True).select_related('company').order_by('-created_at')
        
        # Filter by company if specified
        company_id = self.request.query_params.get('company', None)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        
        # Filter by job type
        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        # Filter by deadline status
        deadline_status = self.request.query_params.get('deadline_status', None)
        if deadline_status == 'active':
            queryset = queryset.filter(application_deadline__gte=timezone.now())
        elif deadline_status == 'expired':
            queryset = queryset.filter(application_deadline__lt=timezone.now())
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get applications for a job posting"""
        job_posting = self.get_object()
        applications = StudentApplication.objects.filter(
            job_posting=job_posting
        ).select_related('student__user').order_by('-applied_at')
        
        serializer = StudentApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific job posting"""
        job_posting = self.get_object()
        
        applications = StudentApplication.objects.filter(job_posting=job_posting)
        
        stats = {
            'total_applications': applications.count(),
            'applications_by_status': {},
            'department_wise_applications': {},
            'average_cgpa_applicants': applications.aggregate(
                avg_cgpa=Avg('student__grades__gpa')
            )['avg_cgpa'] or 0
        }
        
        # Applications by status
        for status_choice in StudentApplication.STATUS_CHOICES:
            status_code = status_choice[0]
            count = applications.filter(status=status_code).count()
            stats['applications_by_status'][status_choice[1]] = count
        
        # Department-wise applications
        dept_counts = applications.values(
            'student__department__name'
        ).annotate(count=Count('id')).order_by('-count')
        
        for dept in dept_counts:
            dept_name = dept['student__department__name']
            stats['department_wise_applications'][dept_name] = dept['count']
        
        return Response(stats)

class StudentApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = StudentApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'student_profile'):
            # Student can see only their applications
            student = self.request.user.student_profile
            return StudentApplication.objects.filter(
                student=student
            ).select_related('job_posting__company').order_by('-applied_at')
        else:
            # Placement officers can see all applications
            return StudentApplication.objects.all().select_related(
                'student__user', 'job_posting__company'
            ).order_by('-applied_at')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update application status (placement officer only)"""
        application = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if new_status not in [choice[0] for choice in StudentApplication.STATUS_CHOICES]:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.notes = notes
        application.save()
        
        return Response({
            'message': f'Application status updated to {application.get_status_display()}',
            'new_status': new_status
        })

class InterviewScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewScheduleSerializer
    permission_classes = [IsPlacementOfficerRole]
    
    def get_queryset(self):
        return InterviewSchedule.objects.all().select_related(
            'application__student__user',
            'application__job_posting__company'
        ).order_by('scheduled_date')
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming interviews"""
        upcoming_interviews = InterviewSchedule.objects.filter(
            scheduled_date__gte=timezone.now(),
            status='scheduled'
        ).select_related(
            'application__student__user',
            'application__job_posting__company'
        ).order_by('scheduled_date')[:10]
        
        serializer = InterviewScheduleSerializer(upcoming_interviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_result(self, request, pk=None):
        """Update interview result"""
        interview = self.get_object()
        result = request.data.get('result')
        feedback = request.data.get('feedback', '')
        
        interview.result = result
        interview.feedback = feedback
        interview.status = 'completed'
        interview.save()
        
        # If selected, update application status
        if result == 'Pass':
            interview.application.status = 'selected'
            interview.application.save()
        
        return Response({
            'message': 'Interview result updated successfully',
            'result': result
        })

class PlacementRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PlacementRecordSerializer
    permission_classes = [IsPlacementOfficerRole]
    
    def get_queryset(self):
        return PlacementRecord.objects.all().select_related(
            'student__user', 'company'
        ).order_by('-placed_at')
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get placement statistics"""
        current_year = timezone.now().year
        academic_year = f"{current_year}-{current_year + 1}"
        
        # Total placements
        total_placements = PlacementRecord.objects.filter(
            is_confirmed=True
        ).count()
        
        # Current year placements
        current_year_placements = PlacementRecord.objects.filter(
            placed_at__year=current_year,
            is_confirmed=True
        ).count()
        
        # Package statistics
        package_stats = PlacementRecord.objects.filter(
            is_confirmed=True
        ).aggregate(
            highest_package=Max('package_offered'),
            lowest_package=Min('package_offered'),
            average_package=Avg('package_offered')
        )
        
        # Department-wise placements
        dept_placements = PlacementRecord.objects.filter(
            is_confirmed=True
        ).values(
            'student__department__name'
        ).annotate(
            count=Count('id'),
            avg_package=Avg('package_offered')
        ).order_by('-count')
        
        # Company-wise placements
        company_placements = PlacementRecord.objects.filter(
            is_confirmed=True
        ).values(
            'company__name'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        stats = {
            'overview': {
                'total_placements': total_placements,
                'current_year_placements': current_year_placements,
                'highest_package': float(package_stats['highest_package']) if package_stats['highest_package'] else 0,
                'lowest_package': float(package_stats['lowest_package']) if package_stats['lowest_package'] else 0,
                'average_package': float(package_stats['average_package']) if package_stats['average_package'] else 0
            },
            'department_wise': [
                {
                    'department': dept['student__department__name'],
                    'placements': dept['count'],
                    'average_package': float(dept['avg_package']) if dept['avg_package'] else 0
                }
                for dept in dept_placements
            ],
            'top_companies': [
                {
                    'company': company['company__name'],
                    'placements': company['count']
                }
                for company in company_placements
            ]
        }
        
        return Response(stats)

class TrainingProgramViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsPlacementOfficerRole]
    
    def get_queryset(self):
        return TrainingProgram.objects.all().order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get enrollments for a training program"""
        program = self.get_object()
        enrollments = TrainingEnrollment.objects.filter(
            program=program
        ).select_related('student__user')
        
        serializer = TrainingEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


# Placement Dashboard API
@api_view(['GET'])
@permission_classes([IsPlacementOfficerRole])
def placement_dashboard_stats(request):
    """Get placement dashboard statistics"""
    try:
        current_year = timezone.now().year
        
        # Basic statistics
        total_companies = Company.objects.filter(is_active=True).count()
        active_job_postings = JobPosting.objects.filter(
            is_active=True,
            application_deadline__gte=timezone.now()
        ).count()
        
        total_placements = PlacementRecord.objects.filter(
            is_confirmed=True
        ).count()
        
        current_year_placements = PlacementRecord.objects.filter(
            placed_at__year=current_year,
            is_confirmed=True
        ).count()
        
        # Application statistics
        total_applications = StudentApplication.objects.count()
        pending_applications = StudentApplication.objects.filter(
            status='applied'
        ).count()
        
        # Interview statistics
        today_interviews = InterviewSchedule.objects.filter(
            scheduled_date__date=timezone.now().date(),
            status='scheduled'
        ).count()
        
        upcoming_interviews = InterviewSchedule.objects.filter(
            scheduled_date__gte=timezone.now(),
            scheduled_date__lte=timezone.now() + timedelta(days=7),
            status='scheduled'
        ).count()
        
        # Package statistics
        package_stats = PlacementRecord.objects.filter(
            is_confirmed=True,
            placed_at__year=current_year
        ).aggregate(
            highest=Max('package_offered'),
            lowest=Min('package_offered'),
            average=Avg('package_offered')
        )
        
        # Recent activities
        recent_placements = PlacementRecord.objects.filter(
            is_confirmed=True
        ).select_related('student__user', 'company').order_by('-placed_at')[:5]
        
        recent_applications = StudentApplication.objects.select_related(
            'student__user', 'job_posting__company'
        ).order_by('-applied_at')[:5]
        
        stats = {
            'overview': {
                'total_companies': total_companies,
                'active_job_postings': active_job_postings,
                'total_placements': total_placements,
                'current_year_placements': current_year_placements,
                'total_applications': total_applications,
                'pending_applications': pending_applications
            },
            'interviews': {
                'today_interviews': today_interviews,
                'upcoming_interviews': upcoming_interviews
            },
            'packages': {
                'highest_package': float(package_stats['highest']) if package_stats['highest'] else 0,
                'lowest_package': float(package_stats['lowest']) if package_stats['lowest'] else 0,
                'average_package': float(package_stats['average']) if package_stats['average'] else 0
            },
            'recent_placements': [
                {
                    'student_name': placement.student.user.get_full_name(),
                    'roll_number': placement.student.roll_number,
                    'company': placement.company.name,
                    'package': float(placement.package_offered),
                    'placed_at': placement.placed_at
                }
                for placement in recent_placements
            ],
            'recent_applications': [
                {
                    'student_name': app.student.user.get_full_name(),
                    'roll_number': app.student.roll_number,
                    'company': app.job_posting.company.name,
                    'position': app.job_posting.title,
                    'status': app.get_status_display(),
                    'applied_at': app.applied_at
                }
                for app in recent_applications
            ]
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate placement dashboard stats: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        # Filter by job type
        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Apply for a job posting"""
        try:
            student = Student.objects.get(user=request.user)
            job_posting = self.get_object()
            
            # Check if already applied
            if StudentApplication.objects.filter(student=student, job_posting=job_posting).exists():
                return Response(
                    {'error': 'Already applied for this position'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check eligibility criteria
            if job_posting.eligible_departments.exists():
                if student.department not in job_posting.eligible_departments.all():
                    return Response(
                        {'error': 'Not eligible - department not in eligible list'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Create application
            application_data = {
                'student': student.id,
                'job_posting': job_posting.id,
                'cover_letter': request.data.get('cover_letter', ''),
                'resume_file': request.data.get('resume_file', '')
            }
            
            serializer = StudentApplicationSerializer(data=application_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class StudentApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = StudentApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return StudentApplication.objects.filter(student=student).order_by('-applied_at')
        except Student.DoesNotExist:
            return StudentApplication.objects.none()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get application statistics for the student"""
        try:
            student = Student.objects.get(user=request.user)
            applications = StudentApplication.objects.filter(student=student)
            
            stats = {
                'total_applications': applications.count(),
                'shortlisted': applications.filter(status='shortlisted').count(),
                'selected': applications.filter(status='selected').count(),
                'rejected': applications.filter(status='rejected').count(),
                'placed': applications.filter(status='placed').count(),
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class PlacementRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlacementRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return PlacementRecord.objects.filter(student=student).order_by('-placed_at')
        except Student.DoesNotExist:
            return PlacementRecord.objects.none()

class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.filter(status__in=['upcoming', 'ongoing'])
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll in a training program"""
        try:
            student = Student.objects.get(user=request.user)
            program = self.get_object()
            
            # Check if already enrolled
            if TrainingEnrollment.objects.filter(student=student, program=program).exists():
                return Response(
                    {'error': 'Already enrolled in this program'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check capacity
            current_enrollments = TrainingEnrollment.objects.filter(program=program).count()
            if current_enrollments >= program.max_participants:
                return Response(
                    {'error': 'Program has reached maximum capacity'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if program is still accepting enrollments
            if program.start_date <= timezone.now().date():
                return Response(
                    {'error': 'Enrollment period has ended'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            enrollment = TrainingEnrollment.objects.create(student=student, program=program)
            serializer = TrainingEnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class TrainingEnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TrainingEnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return TrainingEnrollment.objects.filter(student=student).order_by('-enrolled_at')
        except Student.DoesNotExist:
            return TrainingEnrollment.objects.none()
