from django.contrib import admin
from .models import Category, Text, Translation

# Register your models here.
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
