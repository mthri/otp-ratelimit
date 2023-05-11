from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from register.models import User


class CustomAdmin(admin.AdminSite):
    site_header = _('آچاره')
    site_title = _('مدیریت سامانه آچاره')

admin_site = CustomAdmin()


@admin.register(User, site=admin_site)
class UserAdminNew(UserAdmin):
    search_fields = ('username', 'phone', 'last_name')
    list_display = ('get_full_name', 'phone', 'username')
    ordering = ('-date_joined', )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'project', 'iran_code', 'personnel_code', 'password1', 'password2'),
        }),
    )
    actions = ('download_latest_change', )
    form = UserChangeForm