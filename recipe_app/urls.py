from django.urls import path
from .cbv.cbv import (
    RecipeListCreateView,
    SpinoffListCreateView
)
from . import views

app_name='recipe_app'

urlpatterns=[
    path('', views.home_view, name='home'),
    # path('/recipe/', )
]