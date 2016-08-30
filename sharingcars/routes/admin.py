from django.contrib import admin
from routes.models import Route, CommentRoute


class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


class CommentRouteAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'rating', 'comment')


admin.site.register(Route, RouteAdmin)
admin.site.register(CommentRoute, CommentRouteAdmin)
