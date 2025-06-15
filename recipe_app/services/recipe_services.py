from rest_framework.exceptions import ValidationError
from ..models import Recipe, Spinoff
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
    def create_recipe(recipe):
        parsed_contents = RecipeService._parse_contents(recipe.contents)
        return Recipe.objects.create(
            user=recipe.user,
            title=recipe.title,
            contents=parsed_contents,
            description=recipe.description,
            category=recipe.category,
            image=recipe.image
        )

    @staticmethod
    def create_spinoff(spinoff):
        parsed_contents = RecipeService._parse_contents(spinoff.contents)
        return Spinoff.objects.create(
            user=spinoff.user,
            recipe=spinoff.recipe,
            contents=parsed_contents,
            description=spinoff.description,
            image=spinoff.image
        )

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
