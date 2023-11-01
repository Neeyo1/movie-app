from django import forms
from .models import Movie, Genre, Tag, Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'genres', 'tags']

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