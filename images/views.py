from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User



# Create your views here.
from .models import Image # User
from .serializers import ImageSerializer, UserSerializer, UserImagesSerializer, SingleUserSerializer
from rest_framework import generics, permissions
import json
from .scripts.parse_data import get_image_url
from .scripts.edit_image import * 
import random


class ImageListCreate(generics.ListCreateAPIView):
    def get_queryset(self):
        try:
            limit = self.kwargs['limit']
        except:
            limit = False
        if limit:
            return Image.objects.all().order_by('?')[:self.kwargs['limit']]
        elif self.kwargs['user']:
            return Image.objects.filter(creator=self.kwargs['user'])
        else: 
            return Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [permissions.IsAuthenticated]

# class ImageListCreate(generics.ListCreateAPIView):
#     queryset = Image.objects.filter

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        return super(UserListCreate, self).get_permissions()

class SingleUser(generics.ListAPIView):
    def get_queryset(self):
        username = self.kwargs['username']
        return User.objects.filter(username=username)
    serializer_class = SingleUserSerializer


class GetImageById(generics.ListAPIView):
    def get_queryset(self):
        print(self.kwargs)
        id = self.kwargs['id']
        return Image.objects.filter(id = id)
    serializer_class = ImageSerializer

@csrf_exempt 
def edit(request, id, actions, changes):

    red = green = blue = blur = 0
    brightness = 1
    actions = actions.split(',') 
    changes = changes.split(',')
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

    # Runs edits to image
    def run_edits(image):
        img = open_image(image)

        # sends img to get editors
        if red != 0 or green != 0 or blue != 0:
            img = color(r = red, g = green, b = blue, img = img)
        if blur != 0:
            img = edit_blur(img = img, value = blur)
        if brightness != 1:
            img = edit_brightness(img = img, value = brightness)
        return img

    image = Image.objects.filter(id=id)[0]
    # PUT will overwrite existing file
    if request.method == 'PUT':        
        new_img = run_edits(image)
        image = save_image(new_img, image, create_record=False)
        image_path=get_image_url(request, image)
        image_data = {'path':image_path, 'id':image.id}
        return HttpResponse(json.dumps(image_data))
    
    # POST will create new image
    elif request.method == 'POST':
        new_img = run_edits(image)
    
        image = save_image(new_img, image, create_record=True)
        image_path=get_image_url(request, image)
        image_data = {'path':image_path, 'id':image.id}
        return HttpResponse(json.dumps(image_data))

    else: 
        return HttpResponse('Error! Edits must be made as a PUT or POST request')


def send_file(request,id):
    image = Image.objects.filter(id=id)[0]
    print(f'image_db/{image.path}')
    img = open(f'image_db/{image.path}', 'rb')
    return FileResponse(img, as_attachment=True,filename='new_image.jpeg')

def send_ascii(request, id, html = False):
    if html == 'True':
        html = True
    else:
        html = False
    image = Image.objects.filter(id=id)[0]
    asciiConvert(image, html)
    if html:
        new_file = open(f'image_db/ascii.html', 'rb')
    else:
        new_file = open(f'image_db/ascii.txt', 'rb')
    return FileResponse(new_file, as_attachment=True, filename='ascii.txt')


def crop(request, id, left, top, right, bottom):
    box = (left,top,right, bottom)
    image = Image.objects.filter(id=id)[0]
    img = open_image(image)
    new_img = crop_image(img, box)

    image = save_image(new_img, image, create_record=False)
    image_path=get_image_url(request, image)
    image_data = {'path':image_path, 'id':image.id}
    return HttpResponse(json.dumps(image_data))


def overlay(request, id_1, id_2, left, top):
    image_1 = Image.objects.filter(id=id_1)[0]
    image_2 = Image.objects.filter(id=id_2)[0]
    img_1 = open_image(image_1)
    img_2 = open_image(image_2)
    dest = (left,top)
    new_img = overlay_images(img_1,img_2, dest)
    new_img.show()

    image = save_image(new_img, image, create_record=False)
    image_path=get_image_url(request, image)
    image_data = {'path':image_path, 'id':image.id}
    return HttpResponse(json.dumps(image_data))

