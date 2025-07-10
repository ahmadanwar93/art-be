from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import (LoginSerializer, UserSerializer, RegisterSerializer)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # the DRF token is using database strategy and stateful, compared to stateless for JWT 
        token, _ = Token.objects.get_or_create(user=user)
        # we have to use Token header, not Bearer
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful',
            'status': 'success'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Logout error: {e}")
        return Response({
            'message': 'Logout failed',
            'error': 'Unable to delete authentication token'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)