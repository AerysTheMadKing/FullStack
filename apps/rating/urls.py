from django.urls import path
from . import views

urlpatterns = [
    path('rating/', views.RatingListCreateAPIView.as_view()),
    path('rating/<int:pk>', views.RatingRetrieveUpdateDestroyAPIView.as_view()),
]
