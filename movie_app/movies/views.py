from django.shortcuts import render, HttpResponse
from .models import Genre, Tag, Movie

# Create your views here.
def index(request):
    context = {}
    movies = Movie.objects.all()
    context['movies'] = movies
    return render(request, "movies/index.html", context)