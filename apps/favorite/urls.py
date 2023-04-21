from django.urls import path
from apps.favorite import views

urlpatterns = [
    path('', views.FavoriteCreateView.as_view()),
    path('<int:pk>/', views.FavoriteDeleteView.as_view()),
]