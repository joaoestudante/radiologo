from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from unidecode import unidecode

from radiologo.permissions import IsProgrammingR, IsDirector, IsRadiologoDeveloper, IsTechnicalLogisticR, \
    IsCommunicationMarketingR, IsAdministration, IsUserR
from ..serializers.UserSerializer import UserSerializer
from ..models.user import CustomUser


class ListCreateUsersView(APIView):
    permission_classes = (
        IsAuthenticated, (
                IsAdministration | IsDirector | IsRadiologoDeveloper |
                IsProgrammingR | IsTechnicalLogisticR | IsCommunicationMarketingR
        )
    )

    def get(self, request):
        users = [user for user in CustomUser.objects.all().order_by('author_name')]
        # Sort this way to get proper sorting with UTF8 chars
        users_sorted = sorted(users, key=lambda x: unidecode(''.join(c for c in x.author_name if c.isalnum()).lower()))
        serialized = UserSerializer(users_sorted, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class GetUpdateDeleteUserView(APIView):
    permission_classes = (
        IsAuthenticated, (
                IsAdministration | IsDirector | IsRadiologoDeveloper |
                IsProgrammingR | IsTechnicalLogisticR | IsCommunicationMarketingR |
                IsUserR
        )
    )

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serialized = UserSerializer(user, data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
