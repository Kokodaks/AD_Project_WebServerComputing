from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='recipe_app'

urlpatterns=[
    #HTML 렌더링
    path('', views.home_view, name='home'),
    path('recipe/<int:pk>', views.recipe_detail, name='recipe_detail'),
    path('recipe/spinoff/<int:pk>', views.spinoff_create, name='spinoff_create'),
    path('recipe/spinoff/detail/<int:pk>', views.spinoff_detail, name='spinoff_detail'),
    path('recipe/create', views.recipe_create, name='recipe_create'),
    path('recipe/update/<int:pk>', views.recipe_update, name='recipe_update'),
    path('recipe/spinoff/update/<int:pk>', views.spinoff_update, name='spinoff_update'),
    path('recipe/<int:pk>/delete', views.recipe_delete, name='recipe_delete'),
    path('spinoff/<int:pk>/delete', views.spinoff_delete, name='spinoff_delete'),
    path('like/recipe/<int:pk>/', views.toggle_recipe_like, name='toggle_recipe_like'),
    path('like/spinoff/<int:pk>/', views.toggle_spinoff_like, name='toggle_spinoff_like'),
    path('my-page/', views.my_page, name='my_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
