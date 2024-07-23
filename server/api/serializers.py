from rest_framework import serializers
from .models import Anime, User, user_likedanime

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        '''no one can read password. Write only la'''
        extra_kwargs = {'password':{'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 
        
    
class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['id','name','desc','studios','genres','popularity','score','img']
        extra_kwargs = {'connection':{'read_only':True}}

        def create(self, valididated_data):
            anime = Anime.objects.create(**valididated_data)
            return anime

class UserLikedAnimeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer()

    class Meta:
        model = user_likedanime
        fields = ['id','user','anime','rating','date_liked']

        def create(self, valididated_data):
            m2m = user_likedanime.objects.create(**valididated_data)
            return m2m
        
        def validate(self, attrs):
            if user_likedanime.objects.filter(user=attrs['user'],anime=attrs['anime']).exists():
                raise serializers.ValidationError("The combination of user and anime must be unique.")
            return attrs