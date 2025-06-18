# Libraries
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from common.models import SetupLine
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
import pandas as pd
from django.http import HttpResponse
from loguru import logger
# Serializer for SetupSections model
class SetupLineSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SetupLine
        fields = ['id', 'name', 'created_at','is_deleted','deleted_at']

class SetupLineViewSet(viewsets.ModelViewSet):
    queryset = SetupLine.objects.all()
    serializer_class = SetupLineSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

    def get_queryset(self):
        queryset = SetupLine.objects.all().order_by('-created_at')
        is_deleted = self.request.query_params.get('is_deleted')

        if is_deleted is None :
            is_deleted = 'false'

        queryset = queryset.filter(is_deleted=is_deleted.lower() == 'true')   
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'is_deleted',
                openapi.IN_QUERY,
                description="Filter by deletion status (true/false)",
                type=openapi.TYPE_BOOLEAN,
                default=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

class ExportLineView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'filetype',
                openapi.IN_QUERY,
                description="Specify 'csv' or 'excel' to determine file format",
                type=openapi.TYPE_STRING,
                required=False,
                enum=['csv', 'excel']
            )
        ],
        responses={200: 'File download'}
    )
    def get(self, request):
        filetype = request.GET.get('filetype', 'csv')
        queryset = SetupLine.objects.all().order_by('-created_at').filter(is_deleted=False)
        serializer = SetupLineSerializer(queryset, many=True)
        df = pd.DataFrame(serializer.data)

        if filetype == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=setup_lines.xlsx'
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=setup_lines.csv'
            df.to_csv(path_or_buf=response, index=False)
        return response