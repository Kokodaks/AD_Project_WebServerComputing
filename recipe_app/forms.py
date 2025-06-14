from django import forms
from .models import Recipe, Ingredients

class RecipeForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'contents']

class SpinoffRecipeForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Ingredients
        fields = ['description', 'contents']




