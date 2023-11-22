from django.contrib import admin
from .models import Genre, Tag, Movie, Profile, Comment, Rating

# Register your models here.
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Movie)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Rating)
