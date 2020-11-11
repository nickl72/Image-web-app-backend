# This file will process all requests to edit images
import PIL 

image_path = 'image_db'
def open_image(image):
    return PIL.Image.open(f'{image_path}/{image.path}')

# image is a PIL.Image
def save_image(image):
    image.save(f'{image_path}/new.jpg')
    image.close()
    return


# image is a django database imageField object
def brightness(image,value):
    image = open_image(image)
    return
def blur(image, value):
    image = open_image(image)
    return
def color(image, r=0, g=0, b=0):
    img = open_image(image)
    save_image(img)
    print('image: ', image)
    print('r: ', r)
    print('g: ', g)
    print('b: ', b)

