from email.policy import default
from pyexpat import model
from sqlite3 import Timestamp
from unittest.util import _MAX_LENGTH
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.urls import  reverse
from django_extensions.db.fields import AutoSlugField

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title' ,max_length=255, null=True)

    def __str__(self):
        return self.title
        

class Tag(models.Model):
    name=models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name',max_length=255, null=True)


    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title',max_length=255, null=True)
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')
    thumbnail_image = models.ImageField(upload_to='thumbnailimage/%Y/%m/%d/')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts' ,default=False )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class User(AbstractUser):
    mobile = models.IntegerField(null=True, blank = True)
    email= models.EmailField(unique = True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username



def save(self, *args, **kwargs):
    super(Profile).save()

    img = Image.open(self.avatar.path)

    if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)



class Comment(models.Model): 
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post) 

