from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta, date

from admin_system.models import (
    Staff, Student, Course, Department, Enrollment
)
from student_interface.models import Grade
from .models import (
    TeacherProfile, CourseAssignment, ClassSchedule, 
    Assignment, AssignmentSubmission, Attendance, CounselingSession
)
from .serializers import (
    TeacherProfileSerializer, CourseAssignmentSerializer, ClassScheduleSerializer,
    AssignmentSerializer, AssignmentSubmissionSerializer, AttendanceSerializer,
    CounselingSessionSerializer
)

# Permission Classes
class IsTeacherRole(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        try:
            staff = Staff.objects.get(user=request.user)
            return staff.role == 'TEACHER'
        except Staff.DoesNotExist:
            return False

# Dashboard Stats API
@api_view(['GET'])
@permission_classes([IsTeacherRole])
def teacher_dashboard_stats(request):
    """
    Get teacher dashboard statistics
    """
    try:
        staff = Staff.objects.get(user=request.user)
        teacher_profile, created = TeacherProfile.objects.get_or_create(staff=staff)
        
        # Get course assignments
        course_assignments = CourseAssignment.objects.filter(
            teacher=teacher_profile,
            is_active=True
        )
        
        # Calculate statistics
        total_courses = course_assignments.count()
        total_students = Enrollment.objects.filter(
            course__in=[ca.course for ca in course_assignments],
            is_active=True
        ).count()
        
        # Pending assignments to grade
        pending_grading = AssignmentSubmission.objects.filter(
            assignment__course_assignment__teacher=teacher_profile,
            graded_at__isnull=True
        ).count()
        
        # This week's classes
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        weekly_classes = ClassSchedule.objects.filter(
            course_assignment__teacher=teacher_profile,
            day_of_week__range=[start_of_week.weekday(), end_of_week.weekday()]
        ).count()
        
        # Recent submissions
        recent_submissions = AssignmentSubmission.objects.filter(
            assignment__course_assignment__teacher=teacher_profile,
            submitted_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        stats = {
            'total_courses': total_courses,
            'total_students': total_students,
            'pending_grading': pending_grading,
            'weekly_classes': weekly_classes,
            'recent_submissions': recent_submissions,
            'courses_list': [
                {
                    'id': ca.course.id,
                    'name': ca.course.name,
                    'code': ca.course.code,
                    'students_count': Enrollment.objects.filter(
                        course=ca.course, is_active=True
                    ).count()
                }
                for ca in course_assignments[:5]  # Top 5 courses
            ]
        }
        
        return Response({
            'data': stats,
            'message': 'Teacher dashboard statistics retrieved successfully'
        })
        
    except Staff.DoesNotExist:
        return Response({
            'error': 'Teacher profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Course Assignment ViewSet
class CourseAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAssignmentSerializer
    permission_classes = [IsTeacherRole]
    
    def get_queryset(self):
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            return CourseAssignment.objects.filter(
                teacher=teacher_profile,
                is_active=True
            )
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
            return CourseAssignment.objects.none()
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get students enrolled in this course"""
        course_assignment = self.get_object()
        enrollments = Enrollment.objects.filter(
            course=course_assignment.course,
            is_active=True
        ).select_related('student__user')
        
        students_data = []
        for enrollment in enrollments:
            student_data = {
                'id': enrollment.student.id,
                'name': f"{enrollment.student.user.first_name} {enrollment.student.user.last_name}",
                'email': enrollment.student.user.email,
                'roll_number': enrollment.student.roll_number,
                'enrollment_date': enrollment.enrollment_date,
                'current_grade': enrollment.current_grade
            }
            students_data.append(student_data)
        
        return Response({
            'data': students_data,
            'message': f'Students for {course_assignment.course.name} retrieved successfully'
        })
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """Get class schedule for this course"""
        course_assignment = self.get_object()
        schedules = ClassSchedule.objects.filter(
            course_assignment=course_assignment
        )
        
        serializer = ClassScheduleSerializer(schedules, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Class schedule retrieved successfully'
        })

# Assignment Management ViewSet
class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherRole]
    
    def get_queryset(self):
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            return Assignment.objects.filter(
                course_assignment__teacher=teacher_profile
            ).order_by('-created_at')
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
            return Assignment.objects.none()
    
    def perform_create(self, serializer):
        # Ensure the assignment is created for teacher's course
        course_assignment_id = self.request.data.get('course_assignment')
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            course_assignment = CourseAssignment.objects.get(
                id=course_assignment_id,
                teacher=teacher_profile
            )
            serializer.save(course_assignment=course_assignment)
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist, CourseAssignment.DoesNotExist):
            raise serializers.ValidationError("Invalid course assignment")
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for this assignment"""
        assignment = self.get_object()
        submissions = AssignmentSubmission.objects.filter(
            assignment=assignment
        ).select_related('student__user')
        
        submissions_data = []
        for submission in submissions:
            submission_data = {
                'id': submission.id,
                'student_name': f"{submission.student.user.first_name} {submission.student.user.last_name}",
                'student_roll': submission.student.roll_number,
                'submitted_at': submission.submitted_at,
                'status': submission.status,
                'grade': submission.grade,
                'feedback': submission.feedback,
                'graded_at': submission.graded_at,
                'file_submission': submission.file_submission.url if submission.file_submission else None
            }
            submissions_data.append(submission_data)
        
        return Response({
            'data': submissions_data,
            'message': 'Assignment submissions retrieved successfully'
        })
    
    @action(detail=True, methods=['post'])
    def grade_submission(self, request, pk=None):
        """Grade a specific submission"""
        assignment = self.get_object()
        submission_id = request.data.get('submission_id')
        grade = request.data.get('grade')
        feedback = request.data.get('feedback', '')
        
        try:
            submission = AssignmentSubmission.objects.get(
                id=submission_id,
                assignment=assignment
            )
            
            submission.grade = grade
            submission.feedback = feedback
            submission.graded_at = timezone.now()
            submission.status = 'GRADED'
            submission.save()
            
            # Update course grade if needed
            # This could be expanded to calculate overall course grades
            
            return Response({
                'message': 'Assignment graded successfully',
                'data': {
                    'submission_id': submission.id,
                    'grade': submission.grade,
                    'feedback': submission.feedback
                }
            })
            
        except AssignmentSubmission.DoesNotExist:
            return Response({
                'error': 'Submission not found'
            }, status=status.HTTP_404_NOT_FOUND)

# Attendance Management
@api_view(['GET'])
@permission_classes([IsTeacherRole])
def attendance_list(request):
    """Get attendance records for teacher's courses"""
    try:
        staff = Staff.objects.get(user=request.user)
        teacher_profile = TeacherProfile.objects.get(staff=staff)
        
        # Get attendance records for teacher's courses
        attendance_records = Attendance.objects.filter(
            course_assignment__teacher=teacher_profile
        ).order_by('-date')
        
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Attendance records retrieved successfully'
        })
        
    except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
        return Response({
            'error': 'Teacher profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsTeacherRole])
def mark_attendance(request):
    """Mark attendance for a class"""
    try:
        staff = Staff.objects.get(user=request.user)
        teacher_profile = TeacherProfile.objects.get(staff=staff)
        
        course_assignment_id = request.data.get('course_assignment_id')
        attendance_date = request.data.get('date', timezone.now().date())
        student_attendance = request.data.get('student_attendance', [])  # [{'student_id': 1, 'status': 'PRESENT'}, ...]
        
        # Verify course assignment belongs to teacher
        course_assignment = CourseAssignment.objects.get(
            id=course_assignment_id,
            teacher=teacher_profile
        )
        
        attendance_records = []
        for student_data in student_attendance:
            student_id = student_data.get('student_id')
            attendance_status = student_data.get('status', 'ABSENT')
            
            attendance, created = Attendance.objects.update_or_create(
                course_assignment=course_assignment,
                student_id=student_id,
                date=attendance_date,
                defaults={'status': attendance_status}
            )
            attendance_records.append(attendance)
        
        return Response({
            'message': f'Attendance marked for {len(attendance_records)} students',
            'data': {
                'course': course_assignment.course.name,
                'date': attendance_date,
                'marked_count': len(attendance_records)
            }
        })
        
    except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
        return Response({
            'error': 'Teacher profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except CourseAssignment.DoesNotExist:
        return Response({
            'error': 'Course assignment not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsTeacherRole])
def class_attendance(request):
    """Get attendance for a specific class/course"""
    course_assignment_id = request.query_params.get('course_assignment_id')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    
    try:
        staff = Staff.objects.get(user=request.user)
        teacher_profile = TeacherProfile.objects.get(staff=staff)
        
        # Build query
        attendance_query = Attendance.objects.filter(
            course_assignment__teacher=teacher_profile
        )
        
        if course_assignment_id:
            attendance_query = attendance_query.filter(
                course_assignment_id=course_assignment_id
            )
        
        if date_from:
            attendance_query = attendance_query.filter(date__gte=date_from)
        
        if date_to:
            attendance_query = attendance_query.filter(date__lte=date_to)
        
        attendance_records = attendance_query.order_by('-date')
        
        # Group by date and course
        attendance_summary = {}
        for record in attendance_records:
            date_key = str(record.date)
            course_key = record.course_assignment.course.name
            
            if date_key not in attendance_summary:
                attendance_summary[date_key] = {}
            
            if course_key not in attendance_summary[date_key]:
                attendance_summary[date_key][course_key] = {
                    'present': 0,
                    'absent': 0,
                    'late': 0,
                    'total': 0
                }
            
            attendance_summary[date_key][course_key][record.status.lower()] += 1
            attendance_summary[date_key][course_key]['total'] += 1
        
        return Response({
            'data': attendance_summary,
            'message': 'Class attendance retrieved successfully'
        })
        
    except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
        return Response({
            'error': 'Teacher profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

# Class Schedule ViewSet
class ClassScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ClassScheduleSerializer
    permission_classes = [IsTeacherRole]
    
    def get_queryset(self):
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            return ClassSchedule.objects.filter(
                course_assignment__teacher=teacher_profile
            )
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
            return ClassSchedule.objects.none()

# Counseling Session ViewSet
class CounselingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = CounselingSessionSerializer
    permission_classes = [IsTeacherRole]
    
    def get_queryset(self):
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            return CounselingSession.objects.filter(
                counselor=teacher_profile
            ).order_by('-session_date')
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
            return CounselingSession.objects.none()
    
    def perform_create(self, serializer):
        try:
            staff = Staff.objects.get(user=self.request.user)
            teacher_profile = TeacherProfile.objects.get(staff=staff)
            serializer.save(counselor=teacher_profile)
        except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
            raise serializers.ValidationError("Teacher profile not found")

# Student Performance Analysis
@api_view(['GET'])
@permission_classes([IsTeacherRole])
def student_performance(request):
    """Analyze student performance in teacher's courses"""
    try:
        staff = Staff.objects.get(user=request.user)
        teacher_profile = TeacherProfile.objects.get(staff=staff)
        
        # Get all students in teacher's courses
        course_assignments = CourseAssignment.objects.filter(
            teacher=teacher_profile,
            is_active=True
        )
        
        performance_data = []
        
        for course_assignment in course_assignments:
            # Get enrolled students
            enrollments = Enrollment.objects.filter(
                course=course_assignment.course,
                is_active=True
            ).select_related('student__user')
            
            for enrollment in enrollments:
                student = enrollment.student
                
                # Calculate attendance percentage
                total_classes = Attendance.objects.filter(
                    course_assignment=course_assignment,
                    student=student
                ).count()
                
                present_classes = Attendance.objects.filter(
                    course_assignment=course_assignment,
                    student=student,
                    status='PRESENT'
                ).count()
                
                attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
                
                # Get assignment grades
                assignment_grades = AssignmentSubmission.objects.filter(
                    assignment__course_assignment=course_assignment,
                    student=student,
                    grade__isnull=False
                ).values_list('grade', flat=True)
                
                avg_assignment_grade = sum(assignment_grades) / len(assignment_grades) if assignment_grades else 0
                
                performance_data.append({
                    'student_id': student.id,
                    'student_name': f"{student.user.first_name} {student.user.last_name}",
                    'roll_number': student.roll_number,
                    'course': course_assignment.course.name,
                    'attendance_percentage': round(attendance_percentage, 2),
                    'average_assignment_grade': round(avg_assignment_grade, 2),
                    'total_assignments': len(assignment_grades),
                    'current_grade': enrollment.current_grade
                })
        
        return Response({
            'data': performance_data,
            'message': 'Student performance data retrieved successfully'
        })
        
    except (Staff.DoesNotExist, TeacherProfile.DoesNotExist):
        return Response({
            'error': 'Teacher profile not found'
        }, status=status.HTTP_404_NOT_FOUND)