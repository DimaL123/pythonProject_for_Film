from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.views.generic import ListView, DetailView

from .models import Film,Category, Actor
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


class FilmView(ListView):
    model = Film
    queryset = Film.objects.filter(draft=False)



class FilmDetailView(DetailView):
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

class ActorView(DetailView):
    model = Actor
    template_name = 'filmsapp/actor.html'
    slug_field = "name"