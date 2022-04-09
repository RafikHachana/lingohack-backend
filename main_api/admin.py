from django.contrib import admin
from .models import Category, Text, Translation, Accent, Video

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

@admin.register(Accent)
class AccentAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
