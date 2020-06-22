from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import authentication, permissions
from ..serializers.UserSerializer import UserSerializer
from ..models.user import CustomUser


class ListCreateUsersView(APIView):

    def get(self, request):
        users = [user for user in CustomUser.objects.all()]
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class GetUpdateDeleteUserView(APIView):

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
