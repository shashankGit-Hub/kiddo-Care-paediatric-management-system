from django.contrib import admin
from apps.patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'guardian_name', 'contact_number')
    list_filter = ('gender', 'blood_type', 'is_preterm')
    search_fields = ('first_name', 'last_name', 'guardian_name', 'contact_number', 'email')
    date_hierarchy = 'date_of_birth'

    fieldsets = (
        ('Biographical Profile', {
            'fields': (('first_name', 'last_name'), ('date_of_birth', 'gender'), 'blood_type')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'contact_number', 'email', 'address')
        }),
        ('Medical Context & History', {
            'classes': ('collapse',),
            'fields': ('chronic_conditions', 'allergies', ('is_preterm', 'birth_weight_kg'))
        }),
    )