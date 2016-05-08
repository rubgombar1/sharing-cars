from django.contrib import admin
from common.models import (Administrator, User)

# Register your models here.


class AdministratorAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surnames', 'user_account', 'city', 'searchingCar')


admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(User, UserAdmin)
