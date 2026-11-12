from django.test import TestCase
from rest_framework.test import APIClient

from .models import Anime, User, user_likedanime


class ApiAuthTests(TestCase):
    PROTECTED_ENDPOINTS = [
        ("post", "/api/like_anime/"),
        ("post", "/api/add_to_liked_anime/"),
        ("post", "/api/remove_from_liked_anime/"),
        ("post", "/api/search_anime_from_liked/"),
        ("patch", "/api/search_anime_from_liked/"),
        ("post", "/api/recommendations/"),
        ("post", "/api/favourite_genres/"),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_user(email="alice@example.com", password="alice-pass-123")
        cls.bob = User.objects.create_user(email="bob@example.com", password="bob-pass-123")
        genres = [["Action"], ["Action", "Drama"], ["Comedy"], ["Drama"], ["Comedy", "Romance"], ["Action", "Romance"]]
        cls.anime = [
            Anime.objects.create(
                name=f"Anime {i}", desc="", studios=["Studio"], genres=g,
                popularity=2000 + i, score=6.0 + i * 0.5, img="https://example.com/a.png",
            )
            for i, g in enumerate(genres)
        ]

    def login(self, email, password):
        """Authenticate through the real token endpoint, like the frontend does."""
        client = APIClient()
        res = client.post("/api/token/", {"email": email, "password": password}, format="json")
        self.assertEqual(res.status_code, 200)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
        return client

    def test_protected_endpoints_reject_anonymous_requests(self):
        client = APIClient()
        for method, url in self.PROTECTED_ENDPOINTS:
            with self.subTest(method=method, url=url):
                res = getattr(client, method)(url, {"anime": "Anime 0"}, format="json")
                self.assertEqual(res.status_code, 401)

    def test_register_and_anime_list_stay_public(self):
        client = APIClient()
        self.assertEqual(client.get("/api/anime_list/").status_code, 200)
        res = client.post("/api/user/register/", {"email": "new@example.com", "password": "new-pass-123"}, format="json")
        self.assertEqual(res.status_code, 201)

    def test_name_in_body_cannot_target_another_user(self):
        user_likedanime.objects.create(user=self.bob, anime=self.anime[0])
        alice = self.login("alice@example.com", "alice-pass-123")

        res = alice.post("/api/like_anime/", {"name": "bob@example.com"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

        res = alice.post("/api/add_to_liked_anime/", {"name": "bob@example.com", "anime": "Anime 1"}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(user_likedanime.objects.filter(user=self.alice, anime=self.anime[1]).exists())
        self.assertFalse(user_likedanime.objects.filter(user=self.bob, anime=self.anime[1]).exists())

        res = alice.post("/api/remove_from_liked_anime/", {"name": "bob@example.com", "anime": "Anime 0"}, format="json")
        self.assertEqual(res.status_code, 404)
        self.assertTrue(user_likedanime.objects.filter(user=self.bob, anime=self.anime[0]).exists())

    def test_like_rate_unlike_flow(self):
        alice = self.login("alice@example.com", "alice-pass-123")
        self.assertEqual(alice.post("/api/add_to_liked_anime/", {"anime": "Anime 2"}, format="json").status_code, 201)

        res = alice.post("/api/search_anime_from_liked/", {"anime": "Anime 2"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["user"], self.alice.id)

        res = alice.patch("/api/search_anime_from_liked/", {"anime": "Anime 2", "rating": 8}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["rating"], 8)

        res = alice.post("/api/like_anime/", {}, format="json")
        self.assertEqual([row["anime"]["name"] for row in res.data], ["Anime 2"])

        self.assertEqual(alice.post("/api/remove_from_liked_anime/", {"anime": "Anime 2"}, format="json").status_code, 204)
        self.assertFalse(user_likedanime.objects.filter(user=self.alice).exists())

    def test_missing_anime_or_like_returns_404(self):
        alice = self.login("alice@example.com", "alice-pass-123")
        cases = [
            ("post", "/api/add_to_liked_anime/", {"anime": "No Such Anime"}),
            ("post", "/api/remove_from_liked_anime/", {"anime": "No Such Anime"}),
            ("post", "/api/search_anime_from_liked/", {"anime": "No Such Anime"}),
            ("patch", "/api/search_anime_from_liked/", {"anime": "No Such Anime", "rating": 5}),
            # anime exists, but alice hasn't liked it
            ("post", "/api/remove_from_liked_anime/", {"anime": "Anime 3"}),
            ("patch", "/api/search_anime_from_liked/", {"anime": "Anime 3", "rating": 5}),
        ]
        for method, url, body in cases:
            with self.subTest(method=method, url=url, body=body):
                res = getattr(alice, method)(url, body, format="json")
                self.assertEqual(res.status_code, 404)

    def test_recommendations_and_favourite_genres_use_logged_in_user(self):
        for anime in self.anime[:2]:
            user_likedanime.objects.create(user=self.alice, anime=anime)
        alice = self.login("alice@example.com", "alice-pass-123")

        res = alice.post("/api/favourite_genres/", {}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(set(res.json()["0"]), {"Action", "Drama"})

        res = alice.post("/api/recommendations/", {}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), len(self.anime))
