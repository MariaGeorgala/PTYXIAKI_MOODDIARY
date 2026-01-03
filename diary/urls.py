from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("log/", views.log_mood, name="log_mood"),
    path("history/", views.history_view, name="history"),
    path("stats/", views.stats_view, name="stats"),
    
]
