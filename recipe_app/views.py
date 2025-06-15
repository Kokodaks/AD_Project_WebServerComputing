from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseNotFound, HttpResponseServerError,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.exceptions import ValidationError

from .forms import RecipeForm, SpinoffRecipeForm
from .models import Recipe, Spinoff
from .services.recipe_services import RecipeService

def home_view(request):
    try:
        category = request.GET.get('category', 'food')
        recipes = Recipe.get_recipes_by_category(category)
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'recipe_app/home.html', {
            'recipe_list': page_obj,
            'selected_category': category
        })
    except Exception as e:
        return HttpResponseServerError(f"서버 오류: {e}")


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                recipe = form.save(commit=False)
                recipe.user = request.user
                RecipeService.create_recipe(recipe)
                return redirect('recipe_app:home')  # 302 Redirect
            except ValidationError as e:
                return HttpResponseBadRequest(f"유효성 오류: {e}")
        return HttpResponseBadRequest("폼 유효성 검사 실패")
    else:
        form = RecipeForm()
        return render(request, 'recipe_app/recipe_form.html', {
            'form': form,
            'mode': 'create'
        })


@login_required
def recipe_update(request, pk):
    try:
        recipe = get_object_or_404(Recipe, pk=pk)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("레시피를 찾을 수 없습니다")

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            try:
                RecipeService.update_recipe(recipe, form.cleaned_data)
                return redirect('recipe_app:recipe_detail', pk=recipe.pk)
            except ValidationError as e:
                return HttpResponseBadRequest(f"수정 실패: {e}")
        return HttpResponseBadRequest("폼 유효성 검사 실패")
    else:
        form = RecipeForm(instance=recipe)
        return render(request, 'recipe_app/recipe_form.html', {
            'form': form,
            'mode': 'update',
            'recipe': recipe
        })


@login_required
def spinoff_create(request, pk):
    try:
        recipe = get_object_or_404(Recipe, pk=pk)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("레시피가 존재하지 않습니다.")

    if request.method == 'POST':
        form = SpinoffRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                spinoff = form.save(commit=False)
                spinoff.recipe = recipe
                spinoff.user = request.user
                RecipeService.create_spinoff(spinoff)
                return redirect('recipe_app:spinoff_detail', pk=spinoff.pk)
            except ValidationError as e:
                return HttpResponseBadRequest(f"스핀오프 생성 실패: {e}")
        return HttpResponseBadRequest("폼 유효성 검사 실패")
    else:
        form = SpinoffRecipeForm()
        return render(request, 'recipe_app/spinoff_form.html', {
            'form': form,
            'recipe': recipe,
            'mode': 'create'
        })


@login_required
def spinoff_update(request, pk):
    try:
        spinoff = get_object_or_404(Spinoff, pk=pk)
    except Spinoff.DoesNotExist:
        return HttpResponseNotFound("스핀오프를 찾을 수 없습니다.")

    if request.method == 'POST':
        form = SpinoffRecipeForm(request.POST, request.FILES, instance=spinoff)
        if form.is_valid():
            try:
                RecipeService.update_spinoff(spinoff, form.cleaned_data)
                return redirect('recipe_app:spinoff_detail', pk=spinoff.pk)
            except ValidationError as e:
                return HttpResponseBadRequest(f"스핀오프 수정 실패: {e}")
        return HttpResponseBadRequest("폼 유효성 검사 실패")
    else:
        form = SpinoffRecipeForm(instance=spinoff)
        return render(request, 'recipe_app/spinoff_form.html', {
            'form': form,
            'mode': 'update',
            'recipe': spinoff.recipe
        })


def recipe_detail(request, pk):
    try:
        recipe = get_object_or_404(Recipe, pk=pk)
        spinoff = Spinoff.get_spinoff_by_recipe(recipe)
        return render(request, 'recipe_app/recipe_detail.html', {
            'recipe': recipe,
            'spinoff': spinoff,
        })
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("레시피를 찾을 수 없습니다.")
    except Exception as e:
        return HttpResponseServerError(f"서버 오류: {e}")


def spinoff_detail(request, pk):
    try:
        spinoff = get_object_or_404(Spinoff, pk=pk)
        return render(request, 'recipe_app/spinoff_detail.html', {
            'spinoff': spinoff
        })
    except Spinoff.DoesNotExist:
        return HttpResponseNotFound("스핀오프를 찾을 수 없습니다.")
    except Exception as e:
        return HttpResponseServerError(f"서버 오류: {e}")
