from django import forms
from .models import Movie, Genre, Tag, Comment, Profile
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'genres', 'tags', 'image']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']