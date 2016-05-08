from django.contrib import admin
from routes.models import Route


class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


admin.site.register(Route, RouteAdmin)
