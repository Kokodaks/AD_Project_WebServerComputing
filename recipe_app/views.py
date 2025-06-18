from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden,
    JsonResponse
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.exceptions import ValidationError

from .forms import RecipeForm, SpinoffRecipeForm
from .models import Recipe, Spinoff, Like
from .services.recipe_services import RecipeService

def home_view(request):
    try:
        category = request.GET.get('category', 'food')
        recipes = RecipeService.recipes_by_category(category)
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
                recipe = RecipeService.create_recipe(form, request.user)
                return redirect('recipe_app:recipe_detail', pk=recipe.pk)  # 302 Redirect
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
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.user != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    recipe.delete()
    return redirect("recipe_app:home")

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
                spinoff = RecipeService.create_spinoff(form, recipe, request.user)
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

@login_required
def spinoff_delete(request, pk):
    spinoff = get_object_or_404(Spinoff, pk=pk)
    recipe = spinoff.recipe

    if spinoff.user != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    spinoff.delete()
    return redirect("recipe_app:recipe_detail", pk=recipe.pk)

def recipe_detail(request, pk):
    try:
        recipe = get_object_or_404(Recipe, pk=pk)
        spinoff = RecipeService.get_recipe_spinoff(recipe)
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

@login_required
def toggle_recipe_like(request, pk):
    try:
        result = RecipeService.toggle_recipe_like(request.user, pk)
        return JsonResponse({'liked': result})
    except ObjectDoesNotExist:
        return JsonResponse({'error': '해당 레시피가 존재하지 않습니다.'}, status=404)
    except Exception as e:
        return HttpResponseServerError(f"서버 오류: {str(e)}")


@login_required
def toggle_spinoff_like(request, pk):
    try:
        result = RecipeService.toggle_spinoff_like(request.user, pk)
        return JsonResponse({'liked': result})
    except ObjectDoesNotExist:
        return JsonResponse({'error': '해당 스핀오프가 존재하지 않습니다.'}, status=404)
    except Exception as e:
        return HttpResponseServerError(f"서버 오류: {str(e)}")

@login_required
def my_page(request):
    liked_recipes = RecipeService.get_liked_recipes(request.user)
    liked_spinoffs = RecipeService.get_liked_spinoffs(request.user)
    my_recipes = RecipeService.my_recipes(request.user)
    my_spinoffs = RecipeService.my_spinoffs(request.user)

    return render(request, 'recipe_app/my_page.html', {
        'liked_recipes': liked_recipes,
        'liked_spinoffs': liked_spinoffs,
        'my_recipes': my_recipes,
        'my_spinoffs': my_spinoffs,
    })
