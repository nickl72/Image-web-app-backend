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
        red = green = blue = blur = 0
        brightness = 1
        actions = actions.split(',') 
        changes = changes.split(',')
        print(changes)

        # parses string params
        for i in range(0, len(actions)):
            a = actions[i].lower()
            if a == 'blur':
                blur = int(changes[i])
            elif a == 'brightness':
                brightness = float(changes[i])
            elif a == 'red':
                red = int(changes[i])
            elif a == 'green':
                green = int(changes[i])
            elif a == 'blue':
                blue = int(changes[i])

        image = Image.objects.filter(id=id)[0]
        img = open_image(image)

        # sends img to get editors
        if red != 0 or green != 0 or blue != 0:
            img = color(r = red, g = green, b = blue, img = img)
            img.show()
        if blur != 0:
            img = edit_blur(img = img, value = blur)
            img.show()
        if brightness != 1:
            img = edit_brightness(img = img, value = brightness)
            img.show()
        
        

        image_path=get_image_url(request, image)
        image_data = {'path':image_path, 'id':image.id}
        return HttpResponse(json.dumps(image_data))
    else: 
        return HttpResponse('Error! Edits must be made as a PUT or POST request')

        