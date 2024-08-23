from django.urls import path

from .views import ScoreTable1View, ScoreTable2View

urlpatterns = [
    path('1/', ScoreTable1View.as_view(), name="score-table-1"),
    path('2/', ScoreTable2View.as_view(), name="score-table-2"),
]