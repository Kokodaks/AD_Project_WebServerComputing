from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ..models import Recipe, Spinoff, Like
import json

class RecipeService:

    @staticmethod
    def _parse_contents(contents):
        if isinstance(contents, str):
            try:
                return json.loads(contents)
            except json.JSONDecodeError:
                raise ValidationError("유효하지 않은 JSON 형식입니다.")
        return contents

    @staticmethod
    def recipes_by_category(category):
        return Recipe.get_recipes_by_category(category)

    @staticmethod
    def create_recipe(form, user):
        recipe = form.save(commit=False)
        recipe.user = user
        recipe.contents = RecipeService._parse_contents(recipe.contents)
        recipe.save()
        return recipe

    @staticmethod
    def create_spinoff(form, recipe, user):
        spinoff = form.save(commit=False)
        spinoff.recipe = recipe
        spinoff.user = user
        spinoff.contents = RecipeService._parse_contents(spinoff.contents)
        spinoff.save()
        return spinoff

    @staticmethod
    def update_recipe(recipe, data):
        parsed_contents = RecipeService._parse_contents(data['contents'])

        recipe.title = data['title']
        recipe.description = data['description']
        recipe.category = data['category']
        recipe.contents = parsed_contents

        if data.get('image'):
            recipe.image = data['image']

        recipe.save()
        return recipe

    @staticmethod
    def update_spinoff(spinoff, data):
        parsed_contents = RecipeService._parse_contents(data['contents'])

        spinoff.description = data['description']
        spinoff.contents = parsed_contents

        if data.get('image'):
            spinoff.image = data['image']

        spinoff.save()
        return spinoff

    @staticmethod
    def get_recipe_spinoff(recipe):
        return Spinoff.get_spinoff_by_recipe(recipe)

    @staticmethod
    def get_liked_recipes(user):
        return Recipe.liked_by_user(user)

    @staticmethod
    def get_liked_spinoffs(user):
        return Spinoff.liked_by_user(user)

    @staticmethod
    def toggle_recipe_like(user, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        like, created = Like.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            like.delete()
            return False  # 좋아요 취소
        return True  # 좋아요 추가

    @staticmethod
    def toggle_spinoff_like(user, spinoff_id):
        spinoff = get_object_or_404(Spinoff, pk=spinoff_id)
        like, created = Like.objects.get_or_create(user=user, spinoff=spinoff)
        if not created:
            like.delete()
            return False
        return True

    @staticmethod
    def my_recipes(user):
        recipes = Recipe.objects.filter(user=user)
        return recipes

    @staticmethod
    def my_spinoffs(user):
        spinoffs = Spinoff.objects.filter(user=user)
        return spinoffs

