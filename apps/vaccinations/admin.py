from django.contrib import admin
from apps.vaccinations.models import VaccineDefinition, VaccinationRecord

@admin.register(VaccineDefinition)
class VaccineDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'disease_targeted', 'recommended_offset_days', 'dosage_number')
    list_filter = ('disease_targeted',)

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'vaccine', 'scheduled_date', 'status', 'actual_administered_date')
    list_filter = ('status', 'scheduled_date', 'vaccine')
    search_fields = ('patient__first_name', 'patient__last_name', 'vaccine__name')
    actions = ['mark_as_administered']

    @admin.action(description='Mark selected schedules as Administered')
    def mark_as_administered(self, request, queryset):
        from datetime import date
        queryset.update(status='ADMINISTERED', actual_administered_date=date.today())