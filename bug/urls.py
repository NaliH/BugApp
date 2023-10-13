from django.urls import path
from . import views

app_name = "bug"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("report/", views.report, name="report"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("list/", views.ListView.as_view(), name="list")
]