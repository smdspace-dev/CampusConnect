from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
from .models import Event, EventRegistration, Notification, Report, SystemConfiguration, AuditLog
from .serializers import (EventSerializer, EventRegistrationSerializer, NotificationSerializer,
                        ReportSerializer, SystemConfigurationSerializer, AuditLogSerializer)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Event.objects.annotate(registrations_count=Count('registrations'))
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_time__lte=end_date)
        
        return queryset.order_by('-date_time')
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register a student for an event"""
        event = self.get_object()
        student = getattr(request.user, 'student_profile', None)
        
        if not student:
            return Response(
                {'error': 'Only students can register for events'},
                status=status.HTTP_403_FORBIDDEN
            )
        
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
from datetime import timedelta

from .models import Event, EventRegistration, Notification, Report, SystemConfiguration, AuditLog
from .serializers import (
    EventSerializer, EventRegistrationSerializer, NotificationSerializer,
    ReportSerializer, SystemConfigurationSerializer, AuditLogSerializer
)
from admin_system.models import Student, Staff, Department

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Event.objects.annotate(
            registrations_count=Count('registrations')
        ).select_related('organizer').order_by('-start_date')
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by upcoming events
        upcoming = self.request.query_params.get('upcoming')
        if upcoming == 'true':
            queryset = queryset.filter(start_date__gte=timezone.now())
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register a student for an event"""
        event = self.get_object()
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Only students can register for events'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if registration is required
        if not event.registration_required:
            return Response(
                {'error': 'This event does not require registration'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if registration deadline has passed
        if event.registration_deadline and event.registration_deadline < timezone.now():
            return Response(
                {'error': 'Registration deadline has passed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if event is at capacity
        current_registrations = EventRegistration.objects.filter(
            event=event,
            status__in=['registered', 'confirmed']
        ).count()
        
        if current_registrations >= event.max_participants:
            return Response(
                {'error': 'Event is at full capacity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if student is already registered
        existing_registration = EventRegistration.objects.filter(
            event=event,
            student=student
        ).first()
        
        if existing_registration:
            if existing_registration.status == 'cancelled':
                # Reactivate cancelled registration
                existing_registration.status = 'registered'
                existing_registration.registered_at = timezone.now()
                existing_registration.save()
                return Response({
                    'message': 'Registration reactivated successfully',
                    'registration_id': existing_registration.id
                })
            else:
                return Response(
                    {'error': 'You are already registered for this event'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create new registration
        registration = EventRegistration.objects.create(
            event=event,
            student=student,
            status='registered'
        )
        
        return Response({
            'message': 'Successfully registered for event',
            'registration_id': registration.id,
            'event_title': event.title
        })
    
    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        """Unregister a student from an event"""
        event = self.get_object()
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            registration = EventRegistration.objects.get(
                event=event,
                student=student,
                status__in=['registered', 'confirmed']
            )
            
            registration.status = 'cancelled'
            registration.save()
            
            return Response({
                'message': 'Successfully unregistered from event'
            })
            
        except EventRegistration.DoesNotExist:
            return Response(
                {'error': 'You are not registered for this event'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Get registrations for an event"""
        event = self.get_object()
        registrations = EventRegistration.objects.filter(
            event=event
        ).select_related('student__user').order_by('-registered_at')
        
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        upcoming_events = Event.objects.filter(
            start_date__gte=timezone.now(),
            start_date__lte=timezone.now() + timedelta(days=30)
        ).order_by('start_date')
        
        serializer = EventSerializer(upcoming_events, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Filter notifications for current user
        queryset = Notification.objects.filter(
            Q(is_global=True) |
            Q(target_users=user) |
            Q(recipient_type='all')
        ).distinct().order_by('-created_at')
        
        # Filter by staff/student type
        if hasattr(user, 'staff_profile'):
            queryset = queryset.filter(
                Q(recipient_type__in=['staff', 'all']) |
                Q(target_departments=user.staff_profile.department)
            )
        elif hasattr(user, 'student_profile'):
            queryset = queryset.filter(
                Q(recipient_type__in=['student', 'all']) |
                Q(target_departments=user.student_profile.department)
            )
        
        # Filter by read/unread status
        read_status = self.request.query_params.get('read_status')
        if read_status == 'unread':
            # Exclude notifications that have been read by this user
            queryset = queryset.exclude(reads__user=user)
        elif read_status == 'read':
            # Only notifications that have been read by this user
            queryset = queryset.filter(reads__user=user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        user = request.user
        
        from .models import NotificationRead
        read_record, created = NotificationRead.objects.get_or_create(
            notification=notification,
            user=user
        )
        
        return Response({
            'message': 'Notification marked as read',
            'read_at': read_record.read_at
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        user = request.user
        
        unread_count = Notification.objects.filter(
            Q(is_global=True) |
            Q(target_users=user) |
            Q(recipient_type='all')
        ).exclude(reads__user=user).count()
        
        return Response({'unread_count': unread_count})


# Event Management API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_dashboard_stats(request):
    """Get event dashboard statistics"""
    try:
        # Total events
        total_events = Event.objects.count()
        
        # Upcoming events
        upcoming_events = Event.objects.filter(
            start_date__gte=timezone.now()
        ).count()
        
        # Events this month
        current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
        
        events_this_month = Event.objects.filter(
            start_date__gte=current_month_start,
            start_date__lt=next_month_start
        ).count()
        
        # Events by type
        events_by_type = {}
        for event_type_choice in Event.EVENT_TYPE_CHOICES:
            type_code = event_type_choice[0]
            count = Event.objects.filter(event_type=type_code).count()
            events_by_type[event_type_choice[1]] = count
        
        # Events by status
        events_by_status = {}
        for status_choice in Event.STATUS_CHOICES:
            status_code = status_choice[0]
            count = Event.objects.filter(status=status_code).count()
            events_by_status[status_choice[1]] = count
        
        # Recent registrations
        recent_registrations = EventRegistration.objects.filter(
            registered_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Popular events (by registration count)
        popular_events = Event.objects.annotate(
            reg_count=Count('registrations')
        ).order_by('-reg_count')[:5]
        
        stats = {
            'overview': {
                'total_events': total_events,
                'upcoming_events': upcoming_events,
                'events_this_month': events_this_month,
                'recent_registrations': recent_registrations
            },
            'events_by_type': events_by_type,
            'events_by_status': events_by_status,
            'popular_events': [
                {
                    'title': event.title,
                    'registration_count': event.reg_count,
                    'start_date': event.start_date
                }
                for event in popular_events
            ]
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate event dashboard stats: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        # Check capacity
        if event.max_participants and event.registrations.count() >= event.max_participants:
            return Response(
                {'error': 'Event is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already registered
        if EventRegistration.objects.filter(event=event, student=student).exists():
            return Response(
                {'error': 'Already registered for this event'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration = EventRegistration.objects.create(
            event=event,
            student=student,
            status='registered'
        )
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Get all registrations for an event"""
        event = self.get_object()
        registrations = event.registrations.all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Students can only see their own registrations
        if hasattr(user, 'student_profile'):
            return EventRegistration.objects.filter(student=user.student_profile)
        
        # Staff can see all registrations
        return EventRegistration.objects.all().select_related('event', 'student')
    
    @action(detail=True, methods=['post'])
    def mark_attended(self, request, pk=None):
        """Mark a registration as attended"""
        registration = self.get_object()
        registration.attendance_marked = True
        registration.attended = True
        registration.save()
        
        serializer = self.get_serializer(registration)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Filter notifications for the current user
        if hasattr(user, 'student_profile'):
            return Notification.objects.filter(
                Q(recipient_student=user.student_profile) | 
                Q(recipient_student__isnull=True, recipient_staff__isnull=True)
            ).order_by('-created_at')
        elif hasattr(user, 'staff_profile'):
            return Notification.objects.filter(
                Q(recipient_staff=user.staff_profile) | 
                Q(recipient_student__isnull=True, recipient_staff__isnull=True)
            ).order_by('-created_at')
        
        return Notification.objects.all().order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for current user"""
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True, read_at=timezone.now())
        
        return Response({'message': f'Marked {notifications.count()} notifications as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Report.objects.all().order_by('-created_at')
        
        # Filter by report type if provided
        report_type = self.request.query_params.get('type')
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        
        # Filter by status if provided
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate a report"""
        report = self.get_object()
        
        if report.status == 'generating':
            return Response(
                {'error': 'Report is already being generated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        report.status = 'generating'
        report.save()
        
        # Here you would typically queue a background task to generate the report
        # For now, we'll just mark it as completed
        report.status = 'completed'
        report.save()
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a completed report"""
        report = self.get_object()
        
        if report.status != 'completed' or not report.file_path:
            return Response(
                {'error': 'Report is not ready for download'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # In a real implementation, you would return the file
        return Response({'download_url': f'/media/reports/{report.file_path}'})

class SystemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active configurations"""
        configs = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(configs, many=True)
        return Response(serializer.data)

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = AuditLog.objects.all().order_by('-timestamp')
        
        # Filter by action if provided
        action = self.request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get audit log statistics"""
        total_logs = self.get_queryset().count()
        recent_logs = self.get_queryset().filter(
            timestamp__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        
        action_stats = self.get_queryset().values('action').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        return Response({
            'total_logs': total_logs,
            'recent_logs': recent_logs,
            'top_actions': action_stats
        })
