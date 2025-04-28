from django.contrib import admin
from .models import Account


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'username', 'is_active', 'date_joined')
    list_display_links = ('first_name', 'username', 'email')
    readonly_fields = ('last_joined', 'password')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
