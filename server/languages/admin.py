from django.contrib import admin

# Register your models here.
from .models import Languages


class LanguagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Languages, LanguagesAdmin)