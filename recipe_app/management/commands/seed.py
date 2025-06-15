from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from ...models import Recipe
from ...services.recipe_services import RecipeService
from faker import Faker
import random
import os
import json
import traceback

User = get_user_model()
fake = Faker()
food_dir = os.path.join(settings.MEDIA_ROOT, 'food')
image_files = [f for f in os.listdir(food_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

class Command(BaseCommand):
    help = "Create fake food recipes for users with IDs 1 to 10"

    def handle(self, *args, **kwargs):

        for user_id in range(1, 11):
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"User with id {user_id} does not exist. Skipping."))
                continue

            for _ in range(3):  # 각 사용자당 3개씩 레시피 생성
                image_relative_path = os.path.join('food', random.choice(image_files))
                recipe = Recipe(
                    user=user,
                    title=fake.sentence(nb_words=4),
                    description=fake.paragraph(nb_sentences=2),
                    contents=json.dumps([
                        {"name": fake.word(), "amount": f"{random.randint(15, 100)}"}
                        for _ in range(3)
                    ]),
                    category='food',
                    image=image_relative_path  # 참조만 함
                )

                try:
                    RecipeService.create_recipe(recipe)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"에러 발생: {e}"))
                    traceback.print_exc()

            self.stdout.write(self.style.SUCCESS(f"Created recipes for user {user.username} (ID: {user_id})"))
