from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from apps.patients.models import Patient
from apps.vaccinations.models import VaccineDefinition, VaccinationRecord


@receiver(post_save, sender=Patient)
def generate_patient_vaccination_schedule(sender, instance, created, **kwargs):
    """
    Automated Trigger: Triggers the moment a new Patient row is successfully created in MySQL.
    """
    if created:
        # Fetch all global vaccine definitions
        vaccines = VaccineDefinition.objects.all()
        records_to_create = []

        for vaccine in vaccines:
            # Calculate exact target date dynamically based on the child's birth date
            target_date = instance.date_of_birth + timedelta(days=vaccine.recommended_offset_days)

            records_to_create.append(
                VaccinationRecord(
                    patient=instance,
                    vaccine=vaccine,
                    scheduled_date=target_date,
                    status='PENDING'
                )
            )

        # Bulk create execution for high performance database management
        if records_to_create:
            VaccinationRecord.objects.bulk_create(records_to_create)