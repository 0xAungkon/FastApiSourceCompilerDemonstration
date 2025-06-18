from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .controllers.Authentication.LoginController import LoginAPIView
from .controllers.Common.ProfileController import ProfileAPIView
from .routers.RouterSetup import router as setup_router

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('common/profile', ProfileAPIView.as_view(), name='login'),
    path('setup/', include('common.routers.RouterSetup')),  # include the second router
    
    # Add other authentication-related URLs here if needed
]
