from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Avg
from django.utils import timezone

from .models import (
    ResourcePerson, Workshop, WorkshopRegistration, Consultation, 
    KnowledgeSharingPost, PostInteraction
)
from .serializers import (
    ResourcePersonSerializer, WorkshopSerializer, WorkshopRegistrationSerializer,
    ConsultationSerializer, KnowledgeSharingPostSerializer
)
from admin_system.models import Student

class ResourcePersonViewSet(viewsets.ModelViewSet):
    queryset = ResourcePerson.objects.filter(status='active')
    serializer_class = ResourcePersonSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by person type
        person_type = self.request.query_params.get('person_type', None)
        if person_type:
            queryset = queryset.filter(person_type=person_type)
        
        # Search by expertise
        expertise = self.request.query_params.get('expertise', None)
        if expertise:
            queryset = queryset.filter(expertise_areas__icontains=expertise)
        
        return queryset.order_by('-rating', 'name')

class WorkshopViewSet(viewsets.ModelViewSet):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Workshop.objects.filter(status__in=['planned', 'confirmed', 'ongoing'])
        
        # Filter by workshop type
        workshop_type = self.request.query_params.get('workshop_type', None)
        if workshop_type:
            queryset = queryset.filter(workshop_type=workshop_type)
        
        # Filter upcoming workshops
        upcoming = self.request.query_params.get('upcoming', None)
        if upcoming:
            queryset = queryset.filter(start_date__gte=timezone.now())
        
        return queryset.order_by('start_date')
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register for a workshop"""
        try:
            student = Student.objects.get(user=request.user)
            workshop = self.get_object()
            
            # Check if already registered
            if WorkshopRegistration.objects.filter(student=student, workshop=workshop).exists():
                return Response(
                    {'error': 'Already registered for this workshop'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check capacity
            current_registrations = WorkshopRegistration.objects.filter(workshop=workshop).count()
            if current_registrations >= workshop.max_participants:
                return Response(
                    {'error': 'Workshop has reached maximum capacity'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check registration deadline
            if workshop.registration_deadline < timezone.now():
                return Response(
                    {'error': 'Registration deadline has passed'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            registration = WorkshopRegistration.objects.create(student=student, workshop=workshop)
            serializer = WorkshopRegistrationSerializer(registration)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class WorkshopRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkshopRegistrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return WorkshopRegistration.objects.filter(student=student).order_by('-registered_at')
        except Student.DoesNotExist:
            return WorkshopRegistration.objects.none()

class ConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Consultation.objects.filter(student=student).order_by('-created_at')
        except Student.DoesNotExist:
            return Consultation.objects.none()
    
    def perform_create(self, serializer):
        student = Student.objects.get(user=self.request.user)
        serializer.save(student=student)
    
    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """Get available consultation slots for all resource persons"""
        resource_person_id = request.query_params.get('resource_person', None)
        if not resource_person_id:
            return Response({'error': 'resource_person parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            resource_person = ResourcePerson.objects.get(id=resource_person_id)
            # In a real implementation, this would check the resource person's calendar
            # For now, return sample available slots
            available_slots = [
                {
                    'date': '2024-01-15',
                    'time': '10:00',
                    'available': True
                },
                {
                    'date': '2024-01-15',
                    'time': '14:00',
                    'available': True
                },
                {
                    'date': '2024-01-16',
                    'time': '11:00',
                    'available': False
                }
            ]
            return Response(available_slots, status=status.HTTP_200_OK)
        except ResourcePerson.DoesNotExist:
            return Response({'error': 'Resource person not found'}, status=status.HTTP_404_NOT_FOUND)

class KnowledgeSharingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KnowledgeSharingPostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = KnowledgeSharingPost.objects.filter(status='published')
        
        # Filter by post type
        post_type = self.request.query_params.get('post_type', None)
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        
        # Search in title and content
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a knowledge sharing post"""
        try:
            student = Student.objects.get(user=request.user)
            post = self.get_object()
            
            interaction, created = PostInteraction.objects.get_or_create(
                post=post,
                student=student,
                interaction_type='like'
            )
            
            if created:
                # Update likes count
                post.likes_count += 1
                post.save()
                return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
            else:
                # Unlike
                interaction.delete()
                post.likes_count = max(0, post.likes_count - 1)
                post.save()
                return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
                
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Bookmark a knowledge sharing post"""
        try:
            student = Student.objects.get(user=request.user)
            post = self.get_object()
            
            interaction, created = PostInteraction.objects.get_or_create(
                post=post,
                student=student,
                interaction_type='bookmark'
            )
            
            if created:
                return Response({'status': 'bookmarked'}, status=status.HTTP_201_CREATED)
            else:
                interaction.delete()
                return Response({'status': 'unbookmarked'}, status=status.HTTP_200_OK)
                
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        """Get bookmarked posts for the student"""
        try:
            student = Student.objects.get(user=request.user)
            bookmarks = PostInteraction.objects.filter(
                student=student,
                interaction_type='bookmark'
            ).values_list('post_id', flat=True)
            
            posts = KnowledgeSharingPost.objects.filter(
                id__in=bookmarks,
                status='published'
            ).order_by('-created_at')
            
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
            
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
