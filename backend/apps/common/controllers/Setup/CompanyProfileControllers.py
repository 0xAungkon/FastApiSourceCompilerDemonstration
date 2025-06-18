# import necessary libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.models import ModelDocument, ModelMetaInformation
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend


class CompanyProfileInfoSerializer(serializers.Serializer):
    # Serializer to represent the company profile information
    company_name = serializers.CharField(required=False,max_length=255)
    contact_number = serializers.CharField(required=False,max_length=20)
    email_address = serializers.EmailField(required=False,)
    website_link = serializers.URLField(required=False, allow_blank=True)
    company_address = serializers.CharField(required=False,)
    company_logo = serializers.ImageField(required=False, allow_null=True)
    

# ProfileAPIView handles user profile operations such as retrieving and updating user information
class CompanyProfileAPIView(APIView):

    # Set authentication and permission classes
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # Define schema for the API view
    @swagger_auto_schema(
        operation_description="Get User Profile",
        responses={200: CompanyProfileInfoSerializer()}
    )
    # GET method to retrieve user profile information
    def get(self, request):
        meta_keys = [
            'company_name', 'contact_number', 'email_address',
            'website_link', 'company_address', 'company_logo'
        ] # List of metadata keys to retrieve

        # Fetch metadata from ModelMetaInformation based on the keys
        meta_data = ModelMetaInformation.objects.filter(key__in=meta_keys)
        meta_dict = {item.key: item.value for item in meta_data}
        
        # Prepare the response data
        data = {key: meta_dict.get(key, '') for key in meta_keys}
        
        # If company_logo is present, format it with the request scheme and host
        if data['company_logo']:
            request_scheme = request.scheme
            request_host = request.get_host()
            data['company_logo'] = f"{request_scheme}://{request_host}{data['company_logo']}"
        
        # Return the response with the company profile information
        return Response(data, status=status.HTTP_200_OK)




    
    # Patch method to update company profile information
    @swagger_auto_schema(
        operation_description="Partially Update Company Profile",
        request_body=CompanyProfileInfoSerializer,
        responses={200: CompanyProfileInfoSerializer()}
    )
    def patch(self, request):
        # Initialize the serializer with the request data
        serializer = CompanyProfileInfoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data

            # Check if the document instance is provided
            logo_url = ''
            if data.get('company_logo'):
                # Save the company logo file and get the URL
                logo_file = data.get('company_logo')
                path = default_storage.save(f'meta/{logo_file.name}', ContentFile(logo_file.read()))
                logo_url = default_storage.url(path)
                data['company_logo'] = logo_url

            # Update or create ModelMetaInformation entries based on the provided data
            for key, value in data.items():
                ModelMetaInformation.objects.update_or_create(
                    key=key,
                    defaults={'value': value}
                )
            return self.get(request)  # Call the get method to prepare the latest response data
        
        # If serializer is not valid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)