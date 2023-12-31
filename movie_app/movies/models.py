from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

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
    image = models.ImageField(default='default-movie.png', upload_to='movie_pics')

    def __str__(self):
        return self.name
    
    def is_public(self):
        return self.public
    
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    

class Comment(models.Model):
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_in = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    reply = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    liked_by = models.ManyToManyField(User, related_name='liked_by')

    def __str__(self):
        return self.content
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rate_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    rate_value = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.rate_value)