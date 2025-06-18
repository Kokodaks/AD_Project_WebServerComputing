import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def category_image_upload_path(instance, filename):
    category = instance.category if instance.category else 'uncategorized'
    return os.path.join(category, filename)

def spinoff_image_upload_path(instance, filename):
    category = instance.recipe.category if instance.recipe and instance.recipe.category else 'uncategorized'
    return os.path.join(category, 'spinoff', filename)

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('food', '음식'),
        ('drink', '음료'),
        ('dessert', '디저트')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField()
    contents=models.JSONField()
    image = models.ImageField(upload_to=category_image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_recipes_by_category(cls, category) -> models.QuerySet['Recipe']:
        return cls.objects.filter(category=category).order_by('-created_at')

    @classmethod
    def liked_by_user(cls, user):
        return cls.objects.filter(like__user=user).distinct()

class Spinoff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    contents = models.JSONField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=spinoff_image_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipe.title

    @classmethod
    def get_spinoff_by_recipe(cls, recipe) -> models.QuerySet['Spinoff']:
        return cls.objects.filter(recipe=recipe).order_by('-created_at')

    @classmethod
    def liked_by_user(cls, user):
        return cls.objects.filter(like__user=user).distinct()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.CASCADE)
    spinoff = models.ForeignKey('Spinoff', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'recipe'), ('user', 'spinoff')]

