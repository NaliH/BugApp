from django.urls import path
from . import views

app_name = "bug"
urlpatterns = [
    path("", views.index, name="index"),
    path("report/", views.report, name="report"),
    path("<int:bug_id>/", views.detail, name="detail"),
    path("list/", views.list_bugs, name="list")
]