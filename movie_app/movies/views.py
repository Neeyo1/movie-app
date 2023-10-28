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

def movie_create(request):
    context = {}
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = MovieForm()
    context["form"] = form
    return render(request, "movies/create_edit_form.html", {"form": form})

def movie_edit(request, movie_id):
    context = {}
    movie = get_object_or_404(Movie, pk=movie_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    form = MovieForm(instance=movie)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('movie_detail', args=(str(instance.id))))
    context["form"] = form
    return render(request, "movies/create_edit_form.html", context)

def movie_delete(request, movie_id):
    context = {}
    movie = get_object_or_404(Movie, pk=movie_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    if request.method == "POST":
        movie.delete()
        return HttpResponseRedirect(reverse('index'))
    context["object_to_delete"] = movie
    return render(request, "movies/delete_form.html", context)

def movie_public_private(request, movie_id):
    context = {}
    movie = get_object_or_404(Movie, pk=movie_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")
    
    if request.method == "POST":
        movie.public = not movie.public
        movie.save()
        return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))

    context["object_to_public_private"] = movie
    return render(request, "movies/public_private_form.html", context)