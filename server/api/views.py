from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer, AnimeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Anime, User
import json

# Create your views here.
class CreateUsersView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class AnimeListView(generics.ListAPIView):
    serializer_class = AnimeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        num = self.kwargs.get('num')
        queryset = Anime.objects.all().order_by('-score')[:num]
        return queryset