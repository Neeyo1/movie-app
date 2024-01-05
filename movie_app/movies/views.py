from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import Genre, Tag, Movie, Comment, Rating
from .forms import MovieForm, GenreForm, TagForm, CommentForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.db.models import Count, Sum

# Create your views here.
def index(request):
    context = {}
    #movies = Movie.objects.all()
    #context['movies'] = movies
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
    next_url = request.GET.get('next') or reverse('index')
    return HttpResponseRedirect(next_url)

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

def movie(request):
    context = {}
    if request.user.is_staff:
        movies = Movie.objects.all()
    else:
        movies = Movie.objects.filter(public = True)
    comment_count = []
    movies_with_rating = []
    for movie in movies:
        movie = Movie.objects.filter(name=movie).annotate(avg_rating=Sum('rating__rate_value')/Count('rating'))[0]
        if movie.avg_rating is not None:
            movie.avg_rating = round(movie.avg_rating, 2)
        comments = movie.comment_set.all().count()
        comment_count.append(comments)
        movies_with_rating.append(movie)
    context['movies'] = movies_with_rating
    context['comment_count'] = comment_count
    return render(request, "movies/movie.html", context)

def movie_detail(request, movie_id):
    context = {}
    movie = Movie.objects.filter(id=movie_id).annotate(avg_rating=Sum('rating__rate_value')/Count('rating'))[0]
    if movie.avg_rating is not None:
        movie.avg_rating = round(movie.avg_rating, 2)
    if not movie.public:
        if not request.user.is_staff:
            return HttpResponse("Movie is private")
    comments = movie.comment_set.filter(reply=False).order_by('-created_at')
    if request.user.is_authenticated:
        try:
            user_rating = movie.rating_set.filter(author = request.user)[0].rate_value
        except:
            user_rating = 0
        context["user_rating"] = user_rating
    context["movie"] = movie
    context["comments"] = comments
    return render(request, "movies/movie_detail.html", context)

def movie_create(request):
    context = {}

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")
    
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
        form = MovieForm(request.POST, request.FILES, instance=movie)
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

def genre(request):
    context = {}
    q_genre = request.GET.get('type') or ''
    if q_genre in ('Name', ''):
        genres = Genre.objects.all().order_by('name')
    elif q_genre == 'Movies count':
        genres = Genre.objects.all().annotate(movies=Count('movie')).order_by('movies')
    movie_count = []
    for genre in genres:
        if request.user.is_staff:
            movies = genre.movie_set.all().count()
        else:
            movies = genre.movie_set.filter(public = True).count()
        movie_count.append(movies)
    context['genres'] = genres
    context['movie_count'] = movie_count
    context['q_genre'] = q_genre
    return render(request, "movies/genre.html", context)

def genre_detail(request, genre_id):
    context = {}
    genre = get_object_or_404(Genre, pk=genre_id)
    if request.user.is_staff:
        movies = genre.movie_set.all()
    else:
        movies = genre.movie_set.filter(public = True)
    comment_count = []
    movies_with_rating = []
    for movie in movies:
        movie = Movie.objects.filter(name=movie).annotate(avg_rating=Sum('rating__rate_value')/Count('rating'))[0]
        if movie.avg_rating is not None:
            movie.avg_rating = round(movie.avg_rating, 2)
        comments = movie.comment_set.all().count()
        comment_count.append(comments)
        movies_with_rating.append(movie)
    context["genre"] = genre
    context['movies'] = movies_with_rating
    context['comment_count'] = comment_count
    return render(request, "movies/genre_detail.html", context)

def genre_create(request):
    context = {}

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            #instance = form.save(commit=False)
            #instance.created_by = request.user
            #instance.updated_by = request.user
            #instance.save()
            form.save()
            return HttpResponseRedirect(reverse('genre'))
    else:
        form = GenreForm()
    context["form"] = form
    return render(request, "movies/create_edit_form.html", {"form": form})

def genre_edit(request, genre_id):
    context = {}
    genre = get_object_or_404(Genre, pk=genre_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    form = GenreForm(instance=genre)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('genre_detail', args=(str(instance.id))))
    context["form"] = form
    return render(request, "movies/create_edit_form.html", context)

def genre_delete(request, genre_id):
    context = {}
    genre = get_object_or_404(Genre, pk=genre_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    if request.method == "POST":
        genre.delete()
        return HttpResponseRedirect(reverse('genre'))
    context["object_to_delete"] = genre
    return render(request, "movies/delete_form.html", context)

def tag(request):
    context = {}
    q_tag = request.GET.get('type') or ''
    if q_tag in ('Name', ''):
        tags = Tag.objects.all().order_by('name')
    elif q_tag == 'Movies count':
        tags = Tag.objects.all().annotate(movies=Count('movie')).order_by('movies')
    movie_count = []
    for tag in tags:
        if request.user.is_staff:
            movies = tag.movie_set.all().count()
        else:
            movies = tag.movie_set.filter(public = True).count()
        movie_count.append(movies)
    context['tags'] = tags
    context['movie_count'] = movie_count
    context['q_tag'] = q_tag
    return render(request, "movies/tag.html", context)

def tag_detail(request, tag_id):
    context = {}
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.user.is_staff:
        movies = tag.movie_set.all()
    else:
        movies = tag.movie_set.filter(public = True)
    comment_count = []
    movies_with_rating = []
    for movie in movies:
        movie = Movie.objects.filter(name=movie).annotate(avg_rating=Sum('rating__rate_value')/Count('rating'))[0]
        if movie.avg_rating is not None:
            movie.avg_rating = round(movie.avg_rating, 2)
        comments = movie.comment_set.all().count()
        comment_count.append(comments)
        movies_with_rating.append(movie)
    context["tag"] = tag
    context['movies'] = movies_with_rating
    context['comment_count'] = comment_count
    return render(request, "movies/tag_detail.html", context)

def tag_create(request):
    context = {}

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            #instance = form.save(commit=False)
            #instance.created_by = request.user
            #instance.updated_by = request.user
            #instance.save()
            form.save()
            return HttpResponseRedirect(reverse('tag'))
    else:
        form = TagForm()
    context["form"] = form
    return render(request, "movies/create_edit_form.html", {"form": form})

def tag_edit(request, tag_id):
    context = {}
    tag = get_object_or_404(Tag, pk=tag_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    form = TagForm(instance=tag)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('tag_detail', args=(str(instance.id))))
    context["form"] = form
    return render(request, "movies/create_edit_form.html", context)

def tag_delete(request, tag_id):
    context = {}
    tag = get_object_or_404(Tag, pk=tag_id)

    if not request.user.is_staff:
        return HttpResponse("No rights to do this action")

    if request.method == "POST":
        tag.delete()
        return HttpResponseRedirect(reverse('tag'))
    context["object_to_delete"] = tag
    return render(request, "movies/delete_form.html", context)

def user_profile(request, user_id):
    context = {}
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_staff:
        comments = user.comment_set.all().order_by('-created_at')
    else:
        comments = user.comment_set.filter(created_in__public = True).order_by('-created_at')
    context["user"] = user
    context["comments"] = comments
    return render(request, "movies/user_profile.html", context)

def user_profile_edit(request):
    context = {}

    if not request.user.is_authenticated:
        return HttpResponse("No rights to do this action")
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return HttpResponseRedirect(reverse('user_profile', args=(str(request.user.id))))

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context["u_form"] = u_form
    context["p_form"] = p_form
    return render(request, "movies/user_profile_edit.html", context)

def comment_create(request):
    context = {}

    if not request.user.is_authenticated:
        return HttpResponse("No rights to do this action")
    
    try:
        movie = get_object_or_404(Movie, pk=int(request.GET.get('movie')))
    except:
        return HttpResponse("Invalid movie id given")
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.created_in = movie
            instance.save()
            return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))
    else:
        form = CommentForm()
    context["form"] = form
    return render(request, "movies/create_edit_form.html", {"form": form})

def comment_reply(request):
    context = {}

    if not request.user.is_authenticated:
        return HttpResponse("No rights to do this action")
    
    try:
        movie = get_object_or_404(Movie, pk=int(request.GET.get('movie')))
        comment = get_object_or_404(Comment, pk=int(request.GET.get('comment')))
    except:
        return HttpResponse("Invalid movie or comment id given")
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.created_in = movie
            instance.reply = True
            instance.reply_to = comment
            instance.save()
            return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))
    else:
        form = CommentForm()
    context["form"] = form
    return render(request, "movies/create_edit_form.html", {"form": form})

def comment_like_dislike(request):
    context = {}

    if not request.user.is_authenticated:
        return HttpResponse("No rights to do this action")
    
    try:
        movie = get_object_or_404(Movie, pk=int(request.GET.get('movie')))
        comment = get_object_or_404(Comment, pk=int(request.GET.get('comment')))
    except:
        return HttpResponse("Invalid movie or comment id given")
    
    if request.user == comment.author and not request.user.is_staff:
        return HttpResponse("No rights to do this action")
    
    if request.user in comment.liked_by.all():
        comment.liked_by.remove(request.user)
    else:
        comment.liked_by.add(request.user)
    comment.save()
    return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))

    '''
    if request.method == "POST":
        if request.user in comment.liked_by.all():
            comment.liked_by.remove(request.user)
        else:
            comment.liked_by.add(request.user)
        comment.save()
        return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))
    
    if request.user in comment.liked_by.all():
        action = "dislike"
    else:
        action = "like"
    context["comment"] = comment
    context["action"] = action
    return render(request, "movies/comment_like_dislike_form.html", context)
    '''

def movie_rate(request):
    context = {}

    if not request.user.is_authenticated:
        return HttpResponse("No rights to do this action")
    
    try:
        movie = get_object_or_404(Movie, pk=int(request.GET.get('movie')))
        rate = int(request.GET.get('rate'))
    except:
        return HttpResponse("Invalid movie id or rate value given")
    
    if rate < 1 or rate > 10:
        return HttpResponse("Invalid rate value given")
    
    if movie.rating_set.filter(author = request.user):
        return HttpResponse("You've already rated this movie")
    else:
        rating = Rating(author=request.user, rate_movie=movie, rate_value=rate)
        rating.save()
        return HttpResponseRedirect(reverse('movie_detail', args=(str(movie.id))))