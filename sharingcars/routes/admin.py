from django.contrib import admin
from routes.models import Route, CommentRoute, StopRoute, ApplyRoute


class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'kind', 'user')


class CommentRouteAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'rating', 'comment')


class StopRouteAdmin(admin.ModelAdmin):
    pass


class ApplyRouteAdmin(admin.ModelAdmin):
    pass


admin.site.register(ApplyRoute, ApplyRouteAdmin)
admin.site.register(StopRoute, StopRouteAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(CommentRoute, CommentRouteAdmin)
