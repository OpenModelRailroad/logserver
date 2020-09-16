from django.contrib import admin
from .models import Appsettings


class AppsettingsAdmin(admin.ModelAdmin):
    class Meta:
        model = Appsettings

    list_display = ['key', 'value']


admin.site.register(Appsettings, AppsettingsAdmin)
