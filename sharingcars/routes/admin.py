from django.contrib import admin
from routes.models import Route


class RouteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Route, RouteAdmin)
