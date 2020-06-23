import struct
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core import signing
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from exceptions.radiologoexception import BadInviteTokenException, InvalidTokenException, ExpiredTokenException, \
    InviteAlreadyAcceptedException
from users.models import Invite
from users.serializers.InviteSerializer import InviteSerializer


class InviteAcceptView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        url_token = kwargs["token"]
        try:
            data = signing.TimestampSigner(salt="radiologo").unsign(url_token)
            decoded = signing.b64_decode(data.encode())
            pk = (struct.unpack(str("!i"), decoded[:4])[0], decoded[4:])[0]
        except BadSignature:
            raise BadInviteTokenException
        user = get_object_or_404(get_user_model(), pk=pk)
        invite = Invite.objects.get(invited_user=user)

        self.check_different_token(url_token, invite.sent_token)
        self.check_expired(invite)
        self.check_accepted(invite)

        password = request.data["password"]
        validate_password(password, user=user,
                          password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))

        user.set_password(password)
        invite.accepted = True
        user.is_registered = True
        user.save()
        invite.save()

        return Response(status=status.HTTP_200_OK)

    def check_different_token(self, received_token, sent_token):
        if received_token != sent_token:
            raise InvalidTokenException

    def check_expired(self, invite):
        if invite.last_date_sent + datetime.timedelta(days=settings.INVITE_EXPIRY_DAYS) < timezone.now():
            raise ExpiredTokenException

    def check_accepted(self, invite):
        if invite.accepted:
            raise InviteAlreadyAcceptedException


class InviteListView(generics.ListAPIView):
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()

class InviteResendView(APIView):

    def post(self, request):
        user = get_user_model().objects.get(author_name=request.data["invited_user_author_name"])
        invite = Invite.objects.get(invited_user=user)
        invite.send()

        return Response(InviteSerializer(instance=invite).data, status=status.HTTP_200_OK)