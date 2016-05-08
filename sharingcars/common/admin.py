from django.contrib import admin
from common.models import (Administrator, User)

# Register your models here.


class AdministratorAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(User, UserAdmin)
