# This file will process all requests to edit images
import PIL 

image_path = 'image_db'
def open_image(image):
    return PIL.Image.open(f'{image_path}/{image.path}')


def brightness(image,value):
    return
def blur(image, value):
    return
def color(image, r=0, g=0, b=0):
    image = open_image(image)
    print('image: ', image)
    print('r: ', r)
    print('g: ', g)
    print('b: ', b)

