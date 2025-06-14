from django.shortcuts import render
from .forms import RecipeForm, SpinoffRecipeForm
from rest_framework import viewsets

# Create your views here.
def home_view(request):
    return render(request, 'recipe_app/home.html')
