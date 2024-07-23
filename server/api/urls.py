from django.urls import path, include
from . import views

urlpatterns = [
    path("anime_list/<int:num>", views.AnimeListView.as_view(), name="anime-listing-top-sorted"),
    path("anime_list/", views.AnimeListView.as_view(),name="anime-list"),
    path("like_anime/", views.UserLikedAnimeSearchView.as_view(),name="like-anime"),
    path("add_to_liked_anime/", views.UserLikedAnimeCreateView.as_view(),name="add-to-liked"),
    path("remove_from_liked_anime/", views.UserLikedAnimeDestroyView.as_view(),name="remove-liked"),
    path("search_anime_from_liked/", views.UserLikedAnimeSearchAniView.as_view(),name="search-likedanime-anime-name"),
    path("recommendations/",views.recommendationsView.as_view(),name="get-recommendations"),
    path("favourite_genres/", views.getFavouriteGenresView.as_view(),name="get-favourite-genres") 
]