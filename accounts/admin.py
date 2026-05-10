from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role',
                'student_id',
                'course',
                'year_level',
                'is_approved',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'role',
                'student_id',
                'course',
                'year_level',
                'is_approved',
            )
        }),
    )


try:
    admin.site.unregister(CustomUser)
except:
    pass

admin.site.register(CustomUser, CustomUserAdmin)