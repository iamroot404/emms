from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('staff_number','email','phone_number', 'first_name', 'last_name', 'username', 'is_active','is_staff','is_cook','is_chef','is_admin','is_superadmin')
    list_display_links = ('staff_number','phone_number','email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    odering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.show_description = 'Profile Picture'
    list_display = ('thumbnail', 'staff_number','phone_number', 'user', 'gender','city', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

