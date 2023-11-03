from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movies_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movies_updated')
    public = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    
    def is_public(self):
        return self.public
    

class Comment(models.Model):
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_in = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    reply = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content