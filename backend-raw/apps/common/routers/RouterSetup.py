from rest_framework.routers import DefaultRouter
from django.urls import path, include
from common.controllers.Setup.CompanyProfileControllers import CompanyProfileAPIView
from common.controllers.Setup.SectionControllers import SetupSectionsViewSet
from common.controllers.Setup.LineControllers import SetupLineViewSet, ExportLineView
from common.controllers.Setup.SalaryPackageControllers import SalaryPackageViewSet
from common.controllers.Setup.HolidayControllers import HolidayViewSet
from common.controllers.Setup.DesignationControllers import DesignationViewSet
from utils.Microfunctions import dummy_view

"""Router setup for company profile management
- Company Profile Setup
- Section Setup
- Line Setup
- Salary Package Setup
- Govt. Holiday Setup
"""



router = DefaultRouter()

urlpatterns = [
    path('company-profile/', CompanyProfileAPIView.as_view(), name='login'),
    path('section/', SetupSectionsViewSet.as_view({'get': 'list', 'post': 'create'}), name='sections-list-create'),
    path('section/<uuid:pk>/', SetupSectionsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sections-detail'),
    path('line/', SetupLineViewSet.as_view({'get': 'list', 'post': 'create'}), name='line-list-create'),
    path('line/<uuid:pk>/', SetupLineViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='line-detail'),
    path('salary-package/', SalaryPackageViewSet.as_view({'get': 'list', 'post': 'create'}), name='salary-list-create'),
    path('salary-package/<uuid:pk>/', SalaryPackageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='salary-detail'),
    path('govt-holiday/', HolidayViewSet.as_view({'get': 'list', 'post': 'create'}), name='holiday-list-create'),
    path('govt-holiday/<uuid:pk>/', HolidayViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='holiday-detail'),
    path('designation/', DesignationViewSet.as_view({'get': 'list', 'post': 'create'}), name='designation-create'),
    path('designation/<uuid:pk>/', DesignationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='designation-detail'),
    
    path('export/sections/', dummy_view, name='designation-detail'),
    path('export/designation/', dummy_view, name='designation-detail'),
    path('export/line/', ExportLineView.as_view(), name='designation-detail'),
    path('export/salary-package/', dummy_view, name='designation-detail'),
    path('export/govt-holiday/', dummy_view, name='designation-detail'),
    
]
