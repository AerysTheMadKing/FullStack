from django.urls import path
from favorite import views

urlpatterns = [
    path('', views.FavoriteCreateView.as_view()),
]