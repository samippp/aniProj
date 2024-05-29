from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Anime(models.Model):
    name = models.CharField(max_length=300)
    studios = ArrayField(models.CharField(max_length=60))
    genres = ArrayField(models.CharField(max_length=35))
    popularity = models.IntegerField()
    score = models.FloatField()
    img = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    
class UserManager(BaseUserManager):
    def create_user(self, email, password, liked_anime,**extra_fields):
        if not email:
            raise ValueError("Missing Email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, liked_anime=liked_anime, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("Missing Email")
        
        extra_fields.setdefault("is_superuser", False)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(name="email", unique=True)
    liked_anime = models.ManyToManyField(Anime, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    def __str__(self):
        return self.user
