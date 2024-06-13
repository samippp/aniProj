from django.urls import path, include
from . import views

urlpatterns = [
    path("anime_list/<int:num>", views.AnimeListView.as_view(), name="anime-listing-top-sorted"),
    path("anime_list/", views.AnimeListView.as_view(),name="anime-list"),
    path("like_anime/", views.UserLikedAnimeSearchView.as_view(),name="like-anime")
]