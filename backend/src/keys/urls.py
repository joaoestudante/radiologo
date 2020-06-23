from django.urls import path
from .views.KeyDocView import KeyDocGenerate

urlpatterns = [
    path('new/', KeyDocGenerate.as_view()),
]