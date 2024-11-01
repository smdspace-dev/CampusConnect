# Authentication Views for JWT Login/Logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint that returns JWT tokens
    """
    try:
        # Accept both email and username fields
        email = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email/Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For demo purposes, create a mapping of demo users
        demo_users = {
            'admin@college.edu': {
                'username': 'admin',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User'
            },
            'admin': {
                'username': 'admin',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User'
            },
            'student@college.edu': {
                'username': 'student',
                'role': 'student',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            'student_demo': {
                'username': 'student',
                'role': 'student', 
                'first_name': 'John',
                'last_name': 'Doe'
            },
            'teacher@college.edu': {
                'username': 'teacher',
                'role': 'teacher',
                'first_name': 'Dr. Jane',
                'last_name': 'Smith'
            },
            'teacher_demo': {
                'username': 'teacher',
                'role': 'teacher',
                'first_name': 'Dr. Jane', 
                'last_name': 'Smith'
            },
            'resource@college.edu': {
                'username': 'resource',
                'role': 'resource_person',
                'first_name': 'Resource',
                'last_name': 'Manager'
            },
            'resource_demo': {
                'username': 'resource',
                'role': 'resource_person',
                'first_name': 'Resource',
                'last_name': 'Manager'
            }
        }
        
        # Check if it's a demo user
        if email in demo_users and password in ['admin123', 'student123', 'teacher123', 'resource123']:
            user_data = demo_users[email]
            
            # Try to get or create the user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': email if '@' in email else f"{email}@college.edu",
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True,
                }
            )
            
            if created or not user.check_password(password):
                user.set_password(password)
                user.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user_data['role']
                }
            }, status=status.HTTP_200_OK)
        
        # Try normal authentication
        try:
            username = email.split('@')[0]  # Extract username from email
            user = authenticate(username=username, password=password)
            if not user:
                # Try authenticating with email as username
                user = authenticate(username=email, password=password)
        except:
            user = None
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Determine role based on user groups or other logic
            role = 'student'  # default role
            if user.is_superuser:
                role = 'admin'
            elif hasattr(user, 'profile'):
                role = getattr(user.profile, 'role', 'student')
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': role
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response({
            'error': 'Login failed. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def logout_view(request):
    """
    Logout endpoint that blacklists the refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh token endpoint
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        access_token = token.access_token
        
        return Response({
            'access': str(access_token)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
