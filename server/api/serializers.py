from rest_framework import serializers
from django.contrib.auth.models import User
from .models import anime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        '''no one can read password. Write only la'''
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = anime
        fields = ['name','studios','genres','popularity','score','img','connection']
        extra_kwargs = {'connection':{'read_only':True}}