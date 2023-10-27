from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genres(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Movies(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movies_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movies_updated')
    public = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genres)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name
    
    def is_public(self):
        return self.public