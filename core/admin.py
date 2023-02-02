from django.contrib import admin

from core.models import User


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    empty_value_display = '-empty-'
    exclude = ('password',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name', 'username',)
    readonly_fields = ('date_joined', 'last_login',)

