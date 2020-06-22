from rest_framework import serializers

from users.models import Invite
from users.serializers.UserSerializer import UserSerializer


class InviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invite
        fields = ['invited_user_author_name', 'accepted', 'last_date_sent']