from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.views.generic import ListView, DetailView

from .models import Film,Category, Actor, Genre
from .forms import ReviewForm


# class FilmView(View):
#     def get(self, request):
#         films = Film.objects.all()
#         return render(request, "films/films.html", {"film_list": films})
#
#
# class FilmDetailView(View):
#     def get(self, request, slug):
#         films = Film.objects.get(url=slug)
#         return render(request, "films/film_detail.html", {"films": films})
class GenreYear:
    """Жанри і роки"""
    def get_genres(self):
        return Genre.objects.all()
    def get_years(self):
        return Film.objects.filter(draft=False).values("uear")

class FilmView(GenreYear,ListView):
    model = Film
    queryset = Film.objects.filter(draft=False)



class FilmDetailView(GenreYear,DetailView):
    model = Film
    slug_field = "url"


class AddReviev(View):
    """Відгук"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        film = Film.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))

            form.film = film
            form.save()
        return redirect(film.get_absolute_url())

class ActorView(GenreYear,DetailView):
    model = Actor
    template_name = 'filmsapp/actor.html'
    slug_field = "name"





class FilterFilmList(GenreYear, ListView):
    def get_queryset(self):
        queryset = Film.objects.filter(
            Q(uear__in=self.request.GET.getlist("uear"))|
            Q(genre__in=self.request.GET.getlist("genre"))
        )
        return queryset
