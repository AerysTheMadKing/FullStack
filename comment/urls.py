from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),

    ]


