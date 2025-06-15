from rest_framework import serializers
from .models import Recipe, Spinoff

class RecipeSerializer(serializers.ModelSerializer):
    contents = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    class Meta:
        model = Recipe
        fields = '__all__'

class SpinoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spinoff
        fields = '__all__'

