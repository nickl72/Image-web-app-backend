# This file is used to parse through data structures to build responses for views
import json

def get_image_url(request, image):
    host = request.get_host()
    image_url = f'http://{host}{image.path.url}'
    return image_url