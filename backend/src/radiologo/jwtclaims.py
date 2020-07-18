from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers.UserSerializer import UserSerializer


class RadiologoTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data

class RadiologoTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = RadiologoTokenObtainPairSerializer
