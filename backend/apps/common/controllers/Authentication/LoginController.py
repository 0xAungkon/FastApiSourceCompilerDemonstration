# libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.Microfunctions import is_valid_email

# retrieve the user model
User = get_user_model()

# LoginAPIView handles user login functionality
class LoginAPIView(APIView):
    # define schema for the API view
    @swagger_auto_schema(
        operation_description="Login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response('Login successful'),
            401: openapi.Response('Invalid credentials')
        }
    )

    # POST method to handle user login
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Check if the username is a valid email
        is_email = is_valid_email(username)

        # Authenticate user based on whether the username is an email or not
        if is_email :
            user = User.objects.filter(email=username).first()
            if user:
                username = user.username
            else:
                return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user with the provided credentials
        user = authenticate(username=username, password=password)
        
        # If user is authenticated, generate tokens
        if user:
            # Generate refresh and access tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        # If authentication fails, return an error response
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)