from django import forms
from .models import Recipe, Spinoff
import json

class RecipeForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.HiddenInput())
    image = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'contents', 'image']
        labels = {
            'title': '레시피 제목',
            'image': '사진',
            'category': '카테고리',
            'description': '설명',
            'contents': '재료'
        }

class SpinoffRecipeForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.HiddenInput())
    image = forms.ImageField(required=False)

    class Meta:
        model = Spinoff
        fields = ['description', 'contents', 'image']
        labels = {
            'description' : '설명',
            'contents' : '재료'
        }




