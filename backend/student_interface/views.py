from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from django.utils import timezone
from datetime import timedelta

from .serializers import (
    StudentDashboardSerializer, StudentProfileSerializer, ClubMembershipSerializer,
    GradeSerializer, StudentFeedbackSerializer, StudentAchievementSerializer,
    AssignmentSubmissionSerializer, AttendanceSerializer
)
from .models import StudentProfile, ClubMembership, Grade, StudentFeedback, StudentAchievement
from admin_system.models import Student, Club, Course, Enrollment
from teacher_interface.models import Assignment, AssignmentSubmission, Attendance, CourseAssignment
from common_features.models import Event, EventRegistration

class IsStudentRole(IsAuthenticated):
    """Custom permission class for student-only access"""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        # Check if user has student_profile
        student = getattr(request.user, 'student_profile', None)
        if student:
            return True
        return request.user.is_superuser

class DashboardView(APIView):
    permission_classes = [IsStudentRole]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            student_profile, created = StudentProfile.objects.get_or_create(student=student)
            
            # Current academic year
            current_year = timezone.now().year
            academic_year = f"{current_year}-{current_year + 1}"
            
            # Get enrolled courses
            enrollments = Enrollment.objects.filter(
                student=student,
                academic_year=academic_year,
                is_active=True
            ).select_related('course')
            
            enrolled_courses = [enrollment.course for enrollment in enrollments]
            
            # Get recent grades (last 10)
            recent_grades = Grade.objects.filter(
                student=student,
                academic_year=academic_year
            ).select_related('course').order_by('-created_at')[:10]
            
            # Calculate current GPA
            current_gpa = Grade.objects.filter(
                student=student,
                academic_year=academic_year
            ).aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0
            
            # Get upcoming assignments (next 30 days)
            upcoming_date = timezone.now() + timedelta(days=30)
            course_assignments = CourseAssignment.objects.filter(
                course__in=enrolled_courses,
                semester=student.semester,
                academic_year=academic_year,
                is_active=True
            )
            
            upcoming_assignments = Assignment.objects.filter(
                course_assignment__in=course_assignments,
                due_date__gte=timezone.now(),
                due_date__lte=upcoming_date,
                is_active=True
            ).select_related('course_assignment__course').order_by('due_date')[:5]
            
            # Get attendance summary
            total_classes = Attendance.objects.filter(
                student=student,
                course_assignment__in=course_assignments
            ).count()
            
            present_classes = Attendance.objects.filter(
                student=student,
                course_assignment__in=course_assignments,
                is_present=True
            ).count()
            
            attendance_percentage = round((present_classes / max(total_classes, 1)) * 100, 2)
            
            # Get club memberships
            club_memberships = ClubMembership.objects.filter(
                student=student,
                is_active=True
            ).select_related('club')
            
            # Get upcoming events
            upcoming_events = Event.objects.filter(
                start_date__gte=timezone.now(),
                start_date__lte=timezone.now() + timedelta(days=30),
                target_departments=student.department
            ).order_by('start_date')[:5]
            
            dashboard_data = {
                'student_info': {
                    'name': student.user.get_full_name() or student.user.username,
                    'roll_number': student.roll_number,
                    'department': student.department.name,
                    'year': student.get_year_display(),
                    'semester': student.semester,
                    'current_gpa': round(current_gpa, 2)
                },
                'academic_summary': {
                    'enrolled_courses': len(enrolled_courses),
                    'completed_assignments': AssignmentSubmission.objects.filter(
                        student=student,
                        status__in=['submitted', 'graded']
                    ).count(),
                    'attendance_percentage': attendance_percentage,
                    'current_gpa': round(current_gpa, 2)
                },
                'recent_grades': [
                    {
                        'course_name': grade.course.name,
                        'course_code': grade.course.code,
                        'grade': grade.grade,
                        'total_marks': grade.total_marks,
                        'gpa': float(grade.gpa) if grade.gpa else 0
                    }
                    for grade in recent_grades
                ],
                'upcoming_assignments': [
                    {
                        'id': assignment.id,
                        'title': assignment.title,
                        'course_name': assignment.course_assignment.course.name,
                        'course_code': assignment.course_assignment.course.code,
                        'due_date': assignment.due_date,
                        'max_marks': assignment.max_marks,
                        'status': self.get_assignment_status(assignment, student)
                    }
                    for assignment in upcoming_assignments
                ],
                'club_memberships': [
                    {
                        'club_name': membership.club.name,
                        'position': membership.get_position_display(),
                        'joined_date': membership.joined_date
                    }
                    for membership in club_memberships
                ],
                'upcoming_events': [
                    {
                        'id': event.id,
                        'title': event.title,
                        'start_date': event.start_date,
                        'event_type': event.get_event_type_display(),
                        'venue': event.venue
                    }
                    for event in upcoming_events
                ]
            }
            
            return Response(dashboard_data)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def get_assignment_status(self, assignment, student):
        """Get assignment submission status for student"""
        try:
            submission = AssignmentSubmission.objects.get(
                assignment=assignment,
                student=student
            )
            return submission.status
        except AssignmentSubmission.DoesNotExist:
            return 'pending'


class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return StudentProfile.objects.filter(student=student)
        except Student.DoesNotExist:
            return StudentProfile.objects.none()


class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return ClubMembership.objects.filter(student=student, is_active=True)
        except Student.DoesNotExist:
            return ClubMembership.objects.none()


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Grade.objects.filter(student=student).order_by('-academic_year', 'semester')
        except Student.DoesNotExist:
            return Grade.objects.none()


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Attendance.objects.filter(student=student).order_by('-date')
        except Student.DoesNotExist:
            return Attendance.objects.none()


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            course_assignments = CourseAssignment.objects.filter(
                course__department=student.department,
                semester=student.semester,
                is_active=True
            )
            return Assignment.objects.filter(
                course_assignment__in=course_assignments,
                is_active=True
            ).order_by('-due_date')
        except Student.DoesNotExist:
            return Assignment.objects.none()


class AchievementViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAchievementSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return StudentAchievement.objects.filter(student=student).order_by('-date_achieved')
        except Student.DoesNotExist:
            return StudentAchievement.objects.none()
    
    def perform_create(self, serializer):
        student = Student.objects.get(user=self.request.user)
        serializer.save(student=student)


class StudentCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for student's enrolled courses"""
    permission_classes = [IsStudentRole]
    
    def list(self, request):
        """List student's enrolled courses with additional info"""
        try:
            student = Student.objects.get(user=request.user)
            current_year = timezone.now().year
            academic_year = f"{current_year}-{current_year + 1}"
            
            enrollments = Enrollment.objects.filter(
                student=student,
                academic_year=academic_year,
                is_active=True
            ).select_related('course')
            
            course_data = []
            for enrollment in enrollments:
                course = enrollment.course
                
                # Get course assignment (teacher info)
                course_assignment = CourseAssignment.objects.filter(
                    course=course,
                    semester=student.semester,
                    academic_year=academic_year,
                    is_active=True
                ).first()
                
                # Get student's grade for this course
                grade = Grade.objects.filter(
                    student=student,
                    course=course,
                    academic_year=academic_year
                ).first()
                
                # Get attendance percentage
                total_classes = Attendance.objects.filter(
                    student=student,
                    course_assignment=course_assignment
                ).count() if course_assignment else 0
                
                present_classes = Attendance.objects.filter(
                    student=student,
                    course_assignment=course_assignment,
                    is_present=True
                ).count() if course_assignment else 0
                
                attendance_percentage = round((present_classes / max(total_classes, 1)) * 100, 2)
                
                course_data.append({
                    'id': course.id,
                    'name': course.name,
                    'code': course.code,
                    'description': course.description,
                    'credits': course.credits,
                    'course_type': course.get_course_type_display(),
                    'semester': course.semester,
                    'teacher': {
                        'name': course_assignment.teacher.user.get_full_name() if course_assignment else None,
                        'email': course_assignment.teacher.user.email if course_assignment else None
                    } if course_assignment else None,
                    'grade_info': {
                        'grade': grade.grade if grade else None,
                        'total_marks': grade.total_marks if grade else None,
                        'gpa': float(grade.gpa) if grade and grade.gpa else None
                    } if grade else None,
                    'attendance_percentage': attendance_percentage,
                    'assignment_count': Assignment.objects.filter(
                        course_assignment=course_assignment
                    ).count() if course_assignment else 0
                })
            
            return Response(course_data)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class StudentAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for student assignments"""
    permission_classes = [IsStudentRole]
    
    def list(self, request):
        """List assignments with submission status"""
        try:
            student = Student.objects.get(user=request.user)
            current_year = timezone.now().year
            academic_year = f"{current_year}-{current_year + 1}"
            
            # Get student's course assignments
            enrollments = Enrollment.objects.filter(
                student=student,
                academic_year=academic_year,
                is_active=True
            )
            
            course_assignments = CourseAssignment.objects.filter(
                course__in=[e.course for e in enrollments],
                semester=student.semester,
                academic_year=academic_year,
                is_active=True
            )
            
            assignments = Assignment.objects.filter(
                course_assignment__in=course_assignments,
                is_active=True
            ).select_related('course_assignment__course').order_by('-due_date')
            
            assignment_data = []
            for assignment in assignments:
                # Get submission if exists
                submission = AssignmentSubmission.objects.filter(
                    assignment=assignment,
                    student=student
                ).first()
                
                assignment_data.append({
                    'id': assignment.id,
                    'title': assignment.title,
                    'description': assignment.description,
                    'course_name': assignment.course_assignment.course.name,
                    'course_code': assignment.course_assignment.course.code,
                    'assignment_type': assignment.get_assignment_type_display(),
                    'due_date': assignment.due_date,
                    'max_marks': assignment.max_marks,
                    'created_at': assignment.created_at,
                    'submission_status': submission.status if submission else 'pending',
                    'submitted_at': submission.submitted_at if submission else None,
                    'marks_obtained': submission.marks_obtained if submission else None,
                    'feedback': submission.feedback if submission else None,
                    'can_submit': timezone.now() <= assignment.due_date and (not submission or submission.status == 'pending')
                })
            
            return Response(assignment_data)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit assignment"""
        try:
            student = Student.objects.get(user=request.user)
            assignment = Assignment.objects.get(pk=pk)
            
            # Check if assignment is still open for submission
            if timezone.now() > assignment.due_date:
                return Response(
                    {'error': 'Assignment submission deadline has passed'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            submission_text = request.data.get('submission_text', '')
            file_path = request.data.get('file_path', '')  # Handle file upload separately
            
            # Create or update submission
            submission, created = AssignmentSubmission.objects.update_or_create(
                assignment=assignment,
                student=student,
                defaults={
                    'submission_text': submission_text,
                    'file_path': file_path,
                    'status': 'submitted',
                    'submitted_at': timezone.now()
                }
            )
            
            return Response({
                'message': 'Assignment submitted successfully',
                'submission_id': submission.id,
                'submitted_at': submission.submitted_at
            })
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Assignment.DoesNotExist:
            return Response(
                {'error': 'Assignment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class StudentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for student grades"""
    serializer_class = GradeSerializer
    permission_classes = [IsStudentRole]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Grade.objects.filter(
                student=student
            ).select_related('course').order_by('-academic_year', 'semester')
        except Student.DoesNotExist:
            return Grade.objects.none()
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get grade summary and GPA calculation"""
        try:
            student = Student.objects.get(user=request.user)
            
            # Get all grades
            grades = Grade.objects.filter(student=student).select_related('course')
            
            # Calculate overall GPA
            total_credits = 0
            total_grade_points = 0
            
            semester_gpas = {}
            
            for grade in grades:
                credits = grade.course.credits
                gpa_points = float(grade.gpa) if grade.gpa else 0
                
                total_credits += credits
                total_grade_points += (gpa_points * credits)
                
                # Semester-wise GPA
                semester_key = f"{grade.academic_year}-S{grade.semester}"
                if semester_key not in semester_gpas:
                    semester_gpas[semester_key] = {'credits': 0, 'points': 0, 'grades': []}
                
                semester_gpas[semester_key]['credits'] += credits
                semester_gpas[semester_key]['points'] += (gpa_points * credits)
                semester_gpas[semester_key]['grades'].append({
                    'course_name': grade.course.name,
                    'course_code': grade.course.code,
                    'grade': grade.grade,
                    'gpa': float(grade.gpa) if grade.gpa else 0,
                    'credits': credits
                })
            
            # Calculate semester GPAs
            for semester in semester_gpas:
                semester_data = semester_gpas[semester]
                semester_gpa = (semester_data['points'] / semester_data['credits']) if semester_data['credits'] > 0 else 0
                semester_gpas[semester]['gpa'] = round(semester_gpa, 2)
            
            overall_gpa = (total_grade_points / total_credits) if total_credits > 0 else 0
            
            summary = {
                'overall_gpa': round(overall_gpa, 2),
                'total_credits': total_credits,
                'semester_wise': semester_gpas,
                'grade_distribution': self.get_grade_distribution(grades),
                'performance_trend': self.get_performance_trend(semester_gpas)
            }
            
            return Response(summary)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def get_grade_distribution(self, grades):
        """Calculate grade distribution"""
        distribution = {}
        for grade in grades:
            grade_letter = grade.grade
            if grade_letter in distribution:
                distribution[grade_letter] += 1
            else:
                distribution[grade_letter] = 1
        return distribution
    
    def get_performance_trend(self, semester_gpas):
        """Calculate performance trend"""
        sorted_semesters = sorted(semester_gpas.keys())
        trend = []
        for semester in sorted_semesters:
            trend.append({
                'semester': semester,
                'gpa': semester_gpas[semester]['gpa']
            })
        return trend


# Student Dashboard Stats API
@api_view(['GET'])
@permission_classes([IsStudentRole])
def student_dashboard_stats(request):
    """Get student dashboard statistics"""
    try:
        student = Student.objects.get(user=request.user)
        current_year = timezone.now().year
        academic_year = f"{current_year}-{current_year + 1}"
        
        # Enrolled courses count
        enrolled_courses = Enrollment.objects.filter(
            student=student,
            academic_year=academic_year,
            is_active=True
        ).count()
        
        # Current semester GPA
        current_gpa = Grade.objects.filter(
            student=student,
            academic_year=academic_year,
            semester=student.semester
        ).aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0
        
        # Assignment statistics
        course_assignments = CourseAssignment.objects.filter(
            course__enrollments__student=student,
            course__enrollments__is_active=True,
            semester=student.semester,
            academic_year=academic_year
        )
        
        total_assignments = Assignment.objects.filter(
            course_assignment__in=course_assignments
        ).count()
        
        completed_assignments = AssignmentSubmission.objects.filter(
            student=student,
            assignment__course_assignment__in=course_assignments,
            status__in=['submitted', 'graded']
        ).count()
        
        pending_assignments = total_assignments - completed_assignments
        
        # Attendance statistics
        total_classes = Attendance.objects.filter(
            student=student,
            course_assignment__in=course_assignments
        ).count()
        
        attended_classes = Attendance.objects.filter(
            student=student,
            course_assignment__in=course_assignments,
            is_present=True
        ).count()
        
        attendance_percentage = round((attended_classes / max(total_classes, 1)) * 100, 2)
        
        # Club memberships
        active_memberships = ClubMembership.objects.filter(
            student=student,
            is_active=True
        ).count()
        
        stats = {
            'academic': {
                'enrolled_courses': enrolled_courses,
                'current_gpa': round(current_gpa, 2),
                'total_assignments': total_assignments,
                'completed_assignments': completed_assignments,
                'pending_assignments': pending_assignments,
                'attendance_percentage': attendance_percentage
            },
            'activities': {
                'club_memberships': active_memberships,
                'events_registered': EventRegistration.objects.filter(
                    student=student,
                    status='registered'
                ).count()
            },
            'performance': {
                'overall_gpa': Grade.objects.filter(
                    student=student
                ).aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0,
                'total_credits_earned': Grade.objects.filter(
                    student=student,
                    is_passed=True
                ).aggregate(
                    total_credits=Count('course__credits')
                )['total_credits'] or 0
            }
        }
        
        return Response(stats)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )