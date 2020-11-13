from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Image, User

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'path', 'creator']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'username', 'email', 'password')
    def create(self,data):
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name = data['last_name']     
        )
        user.set_password(data['password'])
        user.save()
        return user

class SingleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserImagesSerializer(serializers.ModelSerializer):
    created_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'created_images']
