from django.contrib import admin
from .models import Genre, Tag, Movie, Profile

# Register your models here.
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Movie)
admin.site.register(Profile)
