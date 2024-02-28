from django import template
from filmsapp.models import Category, Film

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('filmsapp/tags/last_film.html')
def get_last_film(count=5):
    films = Film.objects.order_by("id")[:count]
    return {"last_film": films}
