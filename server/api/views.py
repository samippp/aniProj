from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer, AnimeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Anime, User

# Create your views here.
class CreateUsersView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class AnimeListView(generics.ListAPIView):
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()
    permission_classes = [AllowAny]