from django.contrib import admin

from django.utils.safestring import mark_safe

# Register your models here.
from .models import Category, Actor, Genre, Film, FilmImages, RatingStar, Rating, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", "id")


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class FilmShotsInline(admin.TabularInline):
    model = FilmImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Зображення"


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "uear")
    search_fields = ("title", "category__name")
    inlines = [FilmShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    # fields = (("actors", "director", "genre"),)
    actions = ["unpublish", "publish"]
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("uear", "country", "world_premiere"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "genre", "director", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_usa", "fees_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),

    )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    get_image.short_description = "Зображення"

    ### actions

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запис було оновлено"
        else:
            message_bit = f" {row_update} записів оновлено"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запис було оновлено"
        else:
            message_bit = f" {row_update} записів оновлено"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Публікувати"
    publish.allowed_permission = ('change',)

    unpublish.short_description = " зняти  з публікації"
    unpublish.allowed_permission = ('change',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "film", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "description", "image", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Зображення"


@admin.register(FilmImages)
class FilmImagesAdmin(admin.ModelAdmin):
    list_display = ("title", "film", "get_image")

    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Зображення"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("pi", "star")


admin.site.register(RatingStar)
admin.site.site_title = "Django Films"
admin.site.site_header = "Django Films"
