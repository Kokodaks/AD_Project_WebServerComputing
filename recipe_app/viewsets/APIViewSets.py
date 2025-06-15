from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Recipe, Spinoff
from ..serializers import RecipeSerializer, SpinoffSerializer
import json

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        print("\n🔥 [RecipeViewSet] create() 진입")

        data = {}
        for key in request.data:
            data[key] = request.data.get(key)

        # 이제 JSON 파싱
        if isinstance(data.get('contents'), str):
            try:
                parsed = json.loads(data['contents'])
                print("✅ contents 파싱 성공:", parsed)
                print("📦 파싱된 타입:", type(parsed))
                print("🔎 첫 번째 요소 타입:", type(parsed[0]) if parsed else "빈 리스트")
                data['contents'] = parsed
            except json.JSONDecodeError as e:
                print("❌ contents 파싱 실패:", e)
                return Response(
                    {"contents": "유효한 JSON 형식이 아닙니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)

        # 5. 유효성 검사
        if not serializer.is_valid():
            print("❌ serializer 유효성 검사 실패")
            print("📦 errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 6. 유효성 통과
        print("✅ serializer 유효성 검사 통과")
        print("📦 validated_data:", serializer.validated_data)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpinoffViewSet(viewsets.ModelViewSet):
    queryset = Spinoff.objects.all()
    serializer_class = SpinoffSerializer



