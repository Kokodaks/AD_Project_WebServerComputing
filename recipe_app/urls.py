from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .viewsets.APIViewSets import RecipeViewSet, SpinoffViewSet
from . import views

app_name='recipe_app'

router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('spinoffs', SpinoffViewSet)


urlpatterns=[
    #HTML 렌더링
    path('', views.home_view, name='home'),
    path('recipe/<int:pk>', views.recipe_detail, name='recipe_detail'),
    path('recipe/spinoff/<int:pk>', views.spinoff_create, name='spinoff_create'),
    path('recipe/spinoff/detail/<int:pk>', views.spinoff_detail, name='spinoff_detail'),
    path('recipe/create', views.recipe_create, name='recipe_create'),
    path('recipe/update/<int:pk>', views.recipe_update, name='recipe_update'),
    path('recipe/spinoff/update/<int:pk>', views.spinoff_update, name='spinoff_update'),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
