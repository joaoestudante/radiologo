from django.urls import path
from .views.KeyDocView import KeyDocGenerate, KeyDocInfo

urlpatterns = [
    path('new/', KeyDocGenerate.as_view()),
    path("latest/", KeyDocInfo.as_view())
]