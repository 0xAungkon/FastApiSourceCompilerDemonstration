from rest_framework import viewsets, permissions, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from common.models import SetupSalaryPackage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class SetupSalaryPackageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SetupSalaryPackage
        fields = [
            'package_id',  'house_rent',
            'medical_allowance', 'conveyance', 'food_allowance',
            'created_at', 'is_deleted', 'deleted_at'
        ]

class SalaryPackageViewSet(viewsets.ModelViewSet):
    queryset = SetupSalaryPackage.objects.all()
    serializer_class = SetupSalaryPackageSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']

    def get_queryset(self):
        queryset = SetupSalaryPackage.objects.all().order_by('-created_at')
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
