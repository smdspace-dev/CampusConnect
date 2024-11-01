from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import timedelta

from .serializers import (
    StudentDashboardSerializer, StudentProfileSerializer, ClubMembershipSerializer,
    GradeSerializer, StudentFeedbackSerializer, StudentAchievementSerializer,
    AssignmentSubmissionSerializer, AttendanceSerializer
)
from .models import StudentProfile, ClubMembership, Grade, StudentFeedback, StudentAchievement
from admin_system.models import Student, Club, Course
from teacher_interface.models import Assignment, AssignmentSubmission, Attendance, CourseAssignment
from common_features.models import Event, EventRegistration

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            student_profile, created = StudentProfile.objects.get_or_create(student=student)
            
            # Get recent grades (last 10)
            recent_grades = Grade.objects.filter(student=student).order_by('-created_at')[:10]
            
            # Get upcoming assignments (next 30 days)
            upcoming_date = timezone.now() + timedelta(days=30)
            # Get course assignments for student's department and year
            course_assignments = CourseAssignment.objects.filter(
                course__department=student.department,
                semester=student.semester,
                is_active=True
            )
            upcoming_assignments = Assignment.objects.filter(
                course_assignment__in=course_assignments,
                due_date__gte=timezone.now(),
                due_date__lte=upcoming_date,
                is_active=True
            ).order_by('due_date')[:5]
            
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


class StudentProfileViewSet(viewsets.ModelViewSet):
                    {
                        'id': assignment.id,
                        'title': assignment.title,
                        'course_name': assignment.course_assignment.course.name,
                        'due_date': assignment.due_date,
                        'max_marks': assignment.max_marks,
                        'assignment_type': assignment.assignment_type
                    } for assignment in upcoming_assignments
                ],
                'recent_attendance': AttendanceSerializer(recent_attendance, many=True).data,
                'club_memberships': ClubMembershipSerializer(club_memberships, many=True).data,
                'achievements': StudentAchievementSerializer(achievements, many=True).data,
                'upcoming_events': [
                    {
                        'id': event.id,
                        'title': event.title,
                        'start_date': event.start_date,
                        'venue': event.venue,
                        'event_type': event.event_type
                    } for event in upcoming_events
                ]
            }
            
            return Response(dashboard_data, status=status.HTTP_200_OK)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StudentProfile.objects.filter(student__user=self.request.user)

class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClubMembershipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return ClubMembership.objects.filter(student=student)
        except Student.DoesNotExist:
            return ClubMembership.objects.none()
    
    @action(detail=False, methods=['get'])
    def available_clubs(self, request):
        """Get clubs available for joining"""
        try:
            student = Student.objects.get(user=request.user)
            joined_clubs = ClubMembership.objects.filter(
                student=student, is_active=True
            ).values_list('club_id', flat=True)
            
            available_clubs = Club.objects.filter(
                is_active=True
            ).exclude(id__in=joined_clubs)
            
            club_data = []
            for club in available_clubs:
                current_members = ClubMembership.objects.filter(
                    club=club, is_active=True
                ).count()
                club_data.append({
                    'id': club.id,
                    'name': club.name,
                    'description': club.description,
                    'club_type': club.club_type,
                    'current_members': current_members,
                    'max_members': club.max_members,
                    'can_join': current_members < club.max_members
                })
            
            return Response(club_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def join_club(self, request, pk=None):
        """Join a club"""
        try:
            student = Student.objects.get(user=request.user)
            club = Club.objects.get(pk=pk, is_active=True)
            
            # Check if already a member
            if ClubMembership.objects.filter(student=student, club=club, is_active=True).exists():
                return Response(
                    {'error': 'Already a member of this club'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check capacity
            current_members = ClubMembership.objects.filter(club=club, is_active=True).count()
            if current_members >= club.max_members:
                return Response(
                    {'error': 'Club has reached maximum capacity'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membership = ClubMembership.objects.create(student=student, club=club)
            serializer = ClubMembershipSerializer(membership)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except (Student.DoesNotExist, Club.DoesNotExist):
            return Response({'error': 'Student or Club not found'}, status=status.HTTP_404_NOT_FOUND)

class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Grade.objects.filter(student=student).order_by('-academic_year', 'semester', 'course__name')
        except Student.DoesNotExist:
            return Grade.objects.none()
    
    @action(detail=False, methods=['get'])
    def semester_wise(self, request):
        """Get grades organized by semester"""
        try:
            student = Student.objects.get(user=request.user)
            grades = Grade.objects.filter(student=student).order_by('academic_year', 'semester')
            
            semester_data = {}
            for grade in grades:
                key = f"{grade.academic_year}-Sem{grade.semester}"
                if key not in semester_data:
                    semester_data[key] = []
                semester_data[key].append(GradeSerializer(grade).data)
            
            return Response(semester_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get grade statistics"""
        try:
            student = Student.objects.get(user=request.user)
            grades = Grade.objects.filter(student=student)
            
            if not grades.exists():
                return Response({'message': 'No grades found'}, status=status.HTTP_200_OK)
            
            stats = {
                'total_courses': grades.count(),
                'passed_courses': grades.filter(is_passed=True).count(),
                'failed_courses': grades.filter(is_passed=False).count(),
                'average_gpa': grades.aggregate(avg_gpa=Avg('gpa'))['avg_gpa'] or 0,
                'highest_marks': grades.aggregate(max_marks=max('total_marks'))['max_marks'] or 0,
                'lowest_marks': grades.aggregate(min_marks=min('total_marks'))['min_marks'] or 0
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Attendance.objects.filter(student=student).order_by('-date')
        except Student.DoesNotExist:
            return Attendance.objects.none()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get attendance statistics"""
        try:
            student = Student.objects.get(user=request.user)
            
            # Get attendance for current semester
            current_semester_attendance = Attendance.objects.filter(
                student=student,
                course_assignment__semester=student.semester,
                course_assignment__academic_year='2023-2024'  # Should be dynamic
            )
            
            if not current_semester_attendance.exists():
                return Response({'message': 'No attendance records found'}, status=status.HTTP_200_OK)
            
            total_classes = current_semester_attendance.count()
            attended_classes = current_semester_attendance.filter(is_present=True).count()
            attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
            
            # Course-wise attendance
            course_wise = {}
            for record in current_semester_attendance:
                course_name = record.course_assignment.course.name
                if course_name not in course_wise:
                    course_wise[course_name] = {'total': 0, 'present': 0}
                course_wise[course_name]['total'] += 1
                if record.is_present:
                    course_wise[course_name]['present'] += 1
            
            # Calculate percentage for each course
            for course in course_wise:
                total = course_wise[course]['total']
                present = course_wise[course]['present']
                course_wise[course]['percentage'] = (present / total * 100) if total > 0 else 0
            
            stats = {
                'total_classes': total_classes,
                'attended_classes': attended_classes,
                'missed_classes': total_classes - attended_classes,
                'attendance_percentage': round(attendance_percentage, 2),
                'course_wise_attendance': course_wise
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    
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
    
    def list(self, request):
        """List assignments with submission status"""
        try:
            student = Student.objects.get(user=request.user)
            assignments = self.get_queryset()
            
            assignment_data = []
            for assignment in assignments:
                try:
                    submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
                    submission_data = AssignmentSubmissionSerializer(submission).data
                except AssignmentSubmission.DoesNotExist:
                    submission_data = None
                
                assignment_data.append({
                    'id': assignment.id,
                    'title': assignment.title,
                    'description': assignment.description,
                    'course_name': assignment.course_assignment.course.name,
                    'assignment_type': assignment.assignment_type,
                    'due_date': assignment.due_date,
                    'max_marks': assignment.max_marks,
                    'submission': submission_data
                })
            
            return Response(assignment_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

class AchievementViewSet(viewsets.ModelViewSet):
    serializer_class = StudentAchievementSerializer
    permission_classes = [IsAuthenticated]
    
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
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            current_year = timezone.now().year
            academic_year = f"{current_year}-{current_year + 1}"
            
            enrollments = Enrollment.objects.filter(
                student=student,
                academic_year=academic_year,
                is_active=True
            ).select_related('course')
            
            return [enrollment.course for enrollment in enrollments]
        except Student.DoesNotExist:
            return Course.objects.none()
    
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
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
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
            
            return Assignment.objects.filter(
                course_assignment__in=course_assignments,
                is_active=True
            ).select_related('course_assignment__course').order_by('-due_date')
            
        except Student.DoesNotExist:
            return Assignment.objects.none()
    
    def list(self, request):
        """List assignments with submission status"""
        try:
            student = Student.objects.get(user=request.user)
            assignments = self.get_queryset()
            
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
            assignment = self.get_object()
            
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
