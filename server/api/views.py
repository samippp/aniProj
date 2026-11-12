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
    '''gets all anime sorted by rating. Arg can be passed indicating from 1 anime to num amount of anime'''
    def get_queryset(self):
        num = self.kwargs.get('num')
        queryset = Anime.objects.all().order_by('-score')[:num]
        return queryset
    
class UserLikedAnimeSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        '''gets all the users liked anime'''
        userAnime = user_likedanime.objects.filter(user=request.user).select_related('anime').all()
        serializer = UserLikedAnimeSerializer(userAnime,many=True)
        return Response(serializer.data)

class UserLikedAnimeSearchAniView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        '''gets data from post request'''
        anime_name = request.data.get('anime')   
        if not anime_name:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            '''searches and returns specific instance of user_likedanime. this is used to check if an instance exists'''
            animeOb = Anime.objects.get(name=anime_name)
            userAnime = user_likedanime.objects.filter(user=request.user, anime=animeOb).first()
            serializer = UserLikedAnimeSerializer(userAnime)
            return Response(serializer.data)
        except Anime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self, request, **kwargs):
        '''get patch request payload'''
        anime_name = request.data.get('anime')
        user_rating = request.data.get('rating')
        if not anime_name:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            '''updates previous instance and sets the user_rating'''
            animeOb = Anime.objects.get(name=anime_name)
            userAnimeInstance = user_likedanime.objects.get(user=request.user, anime=animeOb)
            userAnimeInstance.rating = user_rating
            userAnimeInstance.save()
            serializer = UserLikedAnimeSerializer(userAnimeInstance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (Anime.DoesNotExist, user_likedanime.DoesNotExist):
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLikedAnimeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        '''get payload from post'''
        anime = request.data.get('anime')   
        if not anime:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            '''searching for valid anime instance and creates a relationship with the logged in user'''
            animeOb = Anime.objects.get(name=anime)
            instance = user_likedanime.objects.create(
                user=request.user,
                anime = animeOb
            )
            instance.save()
            serializer = UserLikedAnimeSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Anime.DoesNotExist:
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLikedAnimeDestroyView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, **kwargs):
        '''gets payload'''
        anime = request.data.get('anime')   
        if not anime:
            return Response({'error': 'Anime is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            '''searches if it is valid given the data'''
            animeOb = Anime.objects.get(name=anime)
            likedOb = user_likedanime.objects.get(user=request.user,anime=animeOb)
            likedOb.delete()
            return Response("Success",status=status.HTTP_204_NO_CONTENT)
        except (Anime.DoesNotExist, user_likedanime.DoesNotExist):
            return Response({'error': 'Entity not found'}, status=status.HTTP_404_NOT_FOUND)

class getFavouriteGenresView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        import json
        from django.http import JsonResponse
        '''gets the logged in user's liked anime'''
        userAnime = user_likedanime.objects.filter(user=request.user).select_related('anime').all()
        serializer = UserLikedAnimeSerializer(userAnime,many=True)
        '''python script in pandas'''
        res = getFavouriteGenres(serializer.data)
        return JsonResponse(res)
      
class recommendationsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        import json
        from django.http import JsonResponse
        '''gets user liked anime and gets all anime to compare similarity'''
        userAnime = user_likedanime.objects.filter(user=request.user).select_related('anime').all()
        allAnime = Anime.objects.all()
        animeSer = AnimeSerializer(allAnime,many=True)
        serializer = UserLikedAnimeSerializer(userAnime,many=True)
        res = recommend(serializer.data, animeSer.data)
        return JsonResponse(res)