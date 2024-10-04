from django.urls import path, include
from .views import ItemViewSet, CustomTokenObtainPairView, UserRegistrationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    #path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]