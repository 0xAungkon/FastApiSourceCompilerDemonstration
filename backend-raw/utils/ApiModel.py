from rest_framework import status
from ninja.responses import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# Common Response Utility

class ApiResponse:
    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK):
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status_code)

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "status": "error",
            "message": message
        }, status=status_code)
