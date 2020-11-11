from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from .models import Image, User
from .serializers import ImageSerializer, UserSerializer, UserImagesSerializer
from rest_framework import generics
import json
from .scripts.parse_data import get_image_url
from .scripts.edit_image import *

class ImageListCreate(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# class ImageListCreate(generics.ListCreateAPIView):
#     queryset = Image.objects.filter

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserImagesCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    # queryset = User.objects.filter(name__contains = 'nick') # filters results LIKE value
    # queryset = User.objects.all()[:2] # Limits number of results
    serializer_class = UserImagesSerializer

class GetImageById(generics.ListAPIView):
    def get_queryset(self):
        id = self.kwargs['id']
        return Image.objects.filter(id = id)
    serializer_class = ImageSerializer

@csrf_exempt 
def edit(request, id, actions, changes):
    if request.method == 'PUT' or request.method == 'POST':

        print(actions.split(','))
        print(changes.split(','))

        image = Image.objects.filter(id=id)[0]

        # def get_image_url(request, image):
        #     host = request.get_host()
        #     image_url = f'http://{host}{image.path.url}'
        #     return image_url
        color(b=-40, image=image, request=request)
        image_path=get_image_url(request, image)
        image_data = {'path':image_path, 'id':image.id}
        return HttpResponse(json.dumps(image_data))
    else: 
        return HttpResponse('Error! Edits must be made as a PUT or POST request')

        