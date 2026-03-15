from django.urls import path
from .views.station_views import StationListView


urlpatterns = [
    path("", StationListView.as_view(), name="station-list")
]