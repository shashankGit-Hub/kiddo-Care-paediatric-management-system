from django.contrib import admin
from apps.visits.models import Visit

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 1 # Provides one clean blank row automatically for quick data entry
    fields = ('weight_kg', 'height_cm', 'head_circumference_cm', 'clinical_notes')

# Also register standalone for macro data management reviews
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'visit_date', 'weight_kg', 'height_cm', 'head_circumference_cm')
    list_filter = ('visit_date',)
    search_fields = ('patient__first_name', 'patient__last_name')