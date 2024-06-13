from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer, AnimeSerializer, UserLikedAnimeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Anime, User, user_likedanime
from rest_framework.views import APIView
from rest_framework.response import Response
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
    
class UserLikedAnimeSearchView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            userOb = User.objects.get(email=user_name)
            userAnime = user_likedanime.objects.filter(user=userOb).select_related('anime').all()
            serializer = UserLikedAnimeSerializer(userAnime,many=True)
            return Response(serializer.data)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)


