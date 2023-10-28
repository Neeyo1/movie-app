from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import Genre, Tag, Movie
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

# Create your views here.
def index(request):
    context = {}
    movies = Movie.objects.all()
    context['movies'] = movies
    return render(request, "movies/index.html", context)

def login_to_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Success")
            next_url = request.GET.get('next') or reverse('index')
            return HttpResponseRedirect(next_url)
        else:
            error_message = "Incorrect login or password"
            context["error_message"] = error_message
            return render(request, "movies/login_form.html", context)
    return render(request, "movies/login_form.html", context)

def logout_from_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register_to_page(request):
    context = {}
    form = UserCreationForm()
    context["form"] = form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            error_message = "Error during registration"
            context["error_message"] = error_message
            context["form"] = form
            return render(request, "movies/register_form.html", context)
    return render(request, "movies/register_form.html", context)

def movie_detail(request, movie_id):
    context = {}
    movie = get_object_or_404(Movie, pk=movie_id)
    if not movie.public:
        if not request.user.is_staff:
            return HttpResponse("Movie is private")
    context["movie"] = movie
    return render(request, "movies/movie_detail.html", context)