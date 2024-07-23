from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer, AnimeSerializer, UserLikedAnimeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Anime, User, user_likedanime
from rest_framework.views import APIView
from rest_framework.response import Response
from .recommender import recommend, getFavouriteGenres

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

class UserLikedAnimeSearchAniView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        anime_name = request.data.get('anime')   
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not anime_name:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            userOb = User.objects.get(email=user_name)
            animeOb = Anime.objects.get(name=anime_name)
            userAnime = user_likedanime.objects.filter(user=userOb, anime=animeOb).first()
            serializer = UserLikedAnimeSerializer(userAnime)
            return Response(serializer.data)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, **kwargs):
        user_name = request.data.get('name')
        anime_name = request.data.get('anime')
        user_rating = request.data.get('rating')
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not anime_name:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            userOb = User.objects.get(email=user_name)
            animeOb = Anime.objects.get(name=anime_name)
            userAnimeInstance = user_likedanime.objects.get(user=userOb, anime=animeOb)
            userAnimeInstance.rating = user_rating
            userAnimeInstance.save()
            serializer = UserLikedAnimeSerializer(userAnimeInstance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLikedAnimeCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        anime = request.data.get('anime')   
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not anime:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            userOb = User.objects.get(email=user_name)
            animeOb = Anime.objects.get(name=anime)
            instance = user_likedanime.objects.create(
                user=userOb,
                anime = animeOb
            )
            instance.save()
            serializer = UserLikedAnimeSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLikedAnimeDestroyView(APIView):
    permission_classes=[AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        anime = request.data.get('anime')   
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not anime:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            userOb = User.objects.get(email=user_name)
            animeOb = Anime.objects.get(name=anime)
            likedOb = user_likedanime.objects.get(user=userOb,anime=animeOb)
            likedOb.delete()
            return Response("Success",status=status.HTTP_204_NO_CONTENT)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class getFavouriteGenresView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            import json
            from django.http import JsonResponse
            userOb = User.objects.get(email=user_name)
            userAnime = user_likedanime.objects.filter(user=userOb).select_related('anime').all()
            serializer = UserLikedAnimeSerializer(userAnime,many=True)
            res = getFavouriteGenres(serializer.data)
            return JsonResponse(res)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)
      
class recommendationsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        user_name = request.data.get('name')
        if not user_name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            import json
            from django.http import JsonResponse
            userOb = User.objects.get(email=user_name)
            userAnime = user_likedanime.objects.filter(user=userOb).select_related('anime').all()
            serializer = UserLikedAnimeSerializer(userAnime,many=True)
            res = recommend(serializer.data)
            return JsonResponse(res)
        except user_likedanime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)