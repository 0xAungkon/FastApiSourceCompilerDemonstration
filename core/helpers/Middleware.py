# Import necessary modules
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from django.http import HttpResponse
from os import getenv
import base64
import hashlib
import hmac
import json
from loguru import logger
from django.shortcuts import redirect

# Custom middleware to disable CSRF check for all incoming requests
class CsrfExemptMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Disable CSRF check for all incoming requests
        setattr(request, '_dont_enforce_csrf_checks', True)
        return None

# Custom middleware to handle errors and return JSON responses
class HandleErrorsMiddleware(MiddlewareMixin):    
    def process_response(self, request, response):
        # Return the response unchanged if it's successful
        
        if 200 <= response.status_code < 300 or response.status_code == 302:
            return response
        # Handle 3xx redirects
        
        try:
            if response.data and isinstance(response.data, dict):
                return response
        except:
            pass
            
        if isinstance(response, JsonResponse):
            # If it's already a JsonResponse, return it as is
            return response

        error_data = {'detail': ''}

        # Handle 4xx errors (client errors)
        if 400 <= response.status_code < 500:
            if response.status_code == 401:
                error_data['detail'] = 'Authentication required'
            if response.status_code == 404:
                error_data['detail'] = '404 Not Found'
            elif response.status_code == 403:
                error_data['detail'] = 'Authorization required'
            elif response.status_code == 404:
                error_data['detail'] = 'Resource not found'
            elif response.status_code == 429:
                error_data['detail'] = 'Too many requests'
            
        # Handle 5xx errors (server errors)
        elif 500 <= response.status_code < 600:
            error_data['detail'] = 'Server error'

        error_data['detail'] = response.reason_phrase
        # Include the original status code and any content

        # Return a JSON response with the error data
        return JsonResponse(error_data, status=response.status_code)

