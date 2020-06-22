from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RadiologoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['author_name'] = user.author_name

        programs = {}
        for p in user.program_set.all():
            programs[p.pk] = p.name
        token['programs'] = programs

        return token


class RadiologoTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = RadiologoTokenObtainPairSerializer
