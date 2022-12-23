from django.urls import path

from applications.history.api_views.history_views import *

urlpatterns = [
    path("histories/", HistoryListView.as_view()),
    path("histories/<int:pk>/", HistoryDetailView.as_view()),
    path("histories/filters/", HistoryFilterView.as_view()),

    path("histories/get-histories/",GetGreatHistoryById.as_view())
]