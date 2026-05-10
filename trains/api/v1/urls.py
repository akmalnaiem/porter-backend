from django.urls import path
from trains.api.v1.views.train_views import TrainListAPIView

urlpatterns = [
    path("", TrainListAPIView.as_view(), name="train-list")
]