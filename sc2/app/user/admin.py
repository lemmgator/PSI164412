from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, UserProfile, Follow


class UserAdmin(BaseUserAdmin):
    """Class representing user in admin panel"""
    ordering = ['id']
    list_display = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Follow)