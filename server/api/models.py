from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Anime(models.Model):
    name = models.CharField(max_length=300)
    desc = models.TextField()
    studios = ArrayField(models.CharField(max_length=60))
    genres = ArrayField(models.CharField(max_length=35))
    popularity = models.IntegerField()
    score = models.FloatField()
    img = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    
class CustomUserManager(UserManager):
    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("Missing Email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser ,PermissionsMixin):
    email = models.EmailField(name="email", unique=True)
    liked_anime = models.ManyToManyField(Anime, blank=True, through='user_likedanime')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default= False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    def __str__(self):
        return self.user

class user_likedanime(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    position = models.IntegerField()