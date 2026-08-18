from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import CompanyProfile


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role",)}),
    )  # type: ignore


admin.site.register(User, CustomUserAdmin)
admin.site.register(CompanyProfile)