from rest_framework import serializers

#Recipe
class RecipeSpinoffFormSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    contents = serializers.JSONField()

