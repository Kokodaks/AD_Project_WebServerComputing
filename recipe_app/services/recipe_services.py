from ..models import Recipe, Ingredients

class RecipeService:

    @staticmethod
    def create_recipe(user, title, description, contents):
        return Recipe.objects.create(
            user = user,
            title = title,
            contents = contents,
            description = description
        )

    @staticmethod
    def create_spinoff_recipe(user, recipe:Recipe, contents, description):
        return Ingredients.objects.create(
            user = user,
            recipe = recipe,
            contents = contents,
            description = description,
        )
