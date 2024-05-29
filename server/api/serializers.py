from rest_framework import serializers
from .models import Anime, User

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
        fields = ['id','name','studios','genres','popularity','score','img']
        extra_kwargs = {'connection':{'read_only':True}}

