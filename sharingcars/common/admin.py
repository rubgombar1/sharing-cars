from django.contrib import admin
from common.models import (Administrator, User, Comment, Folder)

# Register your models here.


class AdministratorAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surnames', 'user_account', 'city', 'searchingCar')


class CommentAdmin(admin.ModelAdmin):
    pass


class FolderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(User, UserAdmin)
