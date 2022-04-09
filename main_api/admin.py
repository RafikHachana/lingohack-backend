from django.contrib import admin
from .models import Text, Translation

# Register your models here.
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    pass

