from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class KeyDoc(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(default=timezone.now)
    members_when_created = models.IntegerField(default=0)
    doc_hash = models.CharField(max_length=512, default="")
