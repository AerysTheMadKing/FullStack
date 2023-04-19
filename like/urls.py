from django.urls import path
from .views import LikeAPIView, LikeDeleteView, RecommendationApiView

urlpatterns = [
    path('', LikeAPIView.as_view(), name='product_like'),
    path('<int:pk>/', LikeDeleteView.as_view(), name='product_like'),
    path('recommendation/', RecommendationApiView.as_view()),


]