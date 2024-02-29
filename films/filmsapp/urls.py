from django.urls import path

from . import views

urlpatterns = [
    path('', views.FilmView.as_view()),
    path("filter/", views.FilterFilmList.as_view(), name="filter"),
    #path("<slug:slug>/", views.FilmDetailView.as_view()),
    path("<slug:slug>/", views.FilmDetailView.as_view(),name="film_detail"),
    path("review/<int:pk>/", views.AddReviev.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),

]
