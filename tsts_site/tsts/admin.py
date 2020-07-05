from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Question, Answer, T, T_Result


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("question", "image")
    inlines = [AnswerInline]
    save_on_top = True
    save_as = True
    # list_display_links = ("name",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("answer", "image", "id")
    # list_display_links = ("name",)


# admin.site.register(Question)
# admin.site.register(Answer)
admin.site.register(T)
admin.site.register(T_Result)
admin.site.site_title = "Тесты"
admin.site.site_header = "Тесты"
