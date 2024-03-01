from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from django.views.generic import ListView, DetailView

from .models import Film, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


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
        return Film.objects.filter(draft=False).values("uear").distinct()


class FilmView(GenreYear, ListView):
    model = Film
    queryset = Film.objects.filter(draft=False).order_by('id')
    paginate_by = 2


class FilmDetailView(GenreYear, DetailView):
    model = Film
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


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


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'filmsapp/actor.html'
    slug_field = "name"


class FilterFilmList(GenreYear, ListView):
    queryset = Film.objects.order_by('id')
    paginate_by = 3

    def get_queryset(self):
        queryset = Film.objects.filter(
            Q(uear__in=self.request.GET.getlist("uear")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["uear"] = ''.join([f"uear={x}&" for x in self.request.GET.getlist("uear")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                pi=self.get_client_ip(request),
                film_id=int(request.POST.get("film")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
class Search(ListView):
    queryset = Film.objects.order_by('id')
    paginate_by = 1
    def get_queryset(self):
        return Film.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] =f'q={self.request.GET.get("q")}&'

        return context


