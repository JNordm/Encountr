# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser, Profession, Formation, Location, Diplome

from import_export.admin import ImportExportModelAdmin



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ('age', 'profile_image')
    list_display = ('email', 'first_name', 'is_active',)
    list_filter = ('email', 'first_name', 'is_active',)
    fieldsets = (
        ('Informations personnelles', {'fields': ('role', 'first_name', 'last_name',
                                                 'birthdate', 'age', 'profession', 'diplome', 
                                                 'formation', 'location', 'profile_image', 'curriculum_vitae', 
                                                 'contrat' )}),
        ('Informations de contact', {'fields':('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}), ('Key moments', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

class ProfessionAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Profession, ProfessionAdmin)

class FormationAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Formation, FormationAdmin)

class LocationAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Location, LocationAdmin)

class DiplomeAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Diplome, DiplomeAdmin)