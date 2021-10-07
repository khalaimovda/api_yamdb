from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm
from .models import User


class YamdbUserAdmin(UserAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name',
                           'last_name', 'bio', 'role', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name',
                       'last_name', 'bio', 'role', ),
        }),
    )


admin.site.register(User, YamdbUserAdmin)
