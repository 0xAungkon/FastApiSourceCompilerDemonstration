# import necessary libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Define serializers for user profile information and updates
class ProfileInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Define serializer for updating user profile information
class ProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

# ProfileAPIView handles user profile operations such as retrieving and updating user information
class ProfileAPIView(APIView):
    # Set authentication and permission classes
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Define schema for the API view
    @swagger_auto_schema(
        operation_description="Get User Profile",
        responses={200: ProfileInfoSerializer()}
    )
    # GET method to retrieve user profile information
    def get(self, request):
        serializer = ProfileInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT method to update user profile information
    @swagger_auto_schema(
        operation_description="Update User Profile",
        request_body=ProfileUpdateSerializer,
        responses={200: ProfileUpdateSerializer()}
    )
    # Method to handle user profile updates
    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            info_serializer = ProfileInfoSerializer(request.user) # Serialize the updated user information
            return Response(info_serializer.data, status=status.HTTP_200_OK)
        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
