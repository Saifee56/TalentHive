from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from authentication.models import CustomUserModel
from authentication.serializers import CustomUserModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction


class AuthenticationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'], url_path='signup')
    @transaction.atomic
    def sign_up(self, request):
        serializer = CustomUserModelSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Signup failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        # Generate tokens immediately after signup
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "message": "Signup successful",
            "data": {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({
                "success": False,
                "message": "Email and password required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            return Response({
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({
                "success": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)