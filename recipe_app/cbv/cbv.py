from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from ..serializers import RecipeSpinoffFormSerializer
from ..services.recipe_services import RecipeService
from ..models import Recipe, Ingredients


class RecipeListCreateView(GenericAPIView, ListModelMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSpinoffFormSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            recipe = RecipeService.create_recipe(
                user = request.user,
                title = serializer.validated_data['title'],
                description = serializer.validated_data['description'],
                contents = serializer.validated_data['contents']
            )
            return Response({'recipe' : recipe}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpinoffListCreateView(GenericAPIView, ListModelMixin):
    queryset = Ingredients.objects.all()
    serializer_class = RecipeSpinoffFormSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            spinoff_ingredients = RecipeService.create_spinoff_recipe(
                user = request.user,
                recipe = serializer.validated_data['recipe'],
                description = serializer.validated_data['description'],
                contents = serializer.validated_data['contents']
            )
            return Response({'spinoff_ingredients' : spinoff_ingredients}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


