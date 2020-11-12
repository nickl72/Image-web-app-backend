from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Need to add pass field

# class User(models.Model):
#     def __str__(self):
#         return self.username

#     name = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     email = models.EmailField()
#     following = models.ManyToManyField("self", symmetrical = False)
#     password = models.CharField(max_length=200)


class Image(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=254)
    path = models.ImageField(upload_to='')
    description = models.CharField(max_length=254, blank=True)
    edited = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    originals = models.ManyToManyField("self", symmetrical = False)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'created_images') # Consider changing on_delete method to avoid deleting image when a user is deleted
    saved_by = models.ManyToManyField(User, related_name = 'saved_images')

class Tag(models.Model):
    def __str__(self):
        return self.tag

    tag = models.CharField(max_length=200)

class Comment(models.Model):
    def __str__(self):
        return self.comment

    comment = models.CharField(max_length=254)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)