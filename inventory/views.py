from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
import logging

from rest_framework import generics
from rest_framework import status
from .serializers import UserRegistrationSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger('inventory')

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
def retrieve(self, request, pk=None):
        logger.info(f'Fetching item with id {pk}')
        cached_item = cache.get(f'item_{pk}')
        if cached_item:
            logger.debug(f'Item retrieved from cache: {cached_item}')
            return Response(cached_item)
        try:
            item = self.get_object()
            cache.set(f'item_{pk}', ItemSerializer(item).data, timeout=60*15)
            logger.info(f'Item fetched from database: {item}')
            return Response(ItemSerializer(item).data)
        except Item.DoesNotExist:
            logger.error(f'Item with id {pk} not found')
            return Response({"error": "Item not found"}, status=404)
        
        
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)