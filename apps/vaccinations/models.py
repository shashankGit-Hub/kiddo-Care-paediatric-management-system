from django.db import models
from apps.patients.models import Patient


class VaccineDefinition(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., BCG, HepB, DTaP-IPV-HepB-Hib")
    disease_targeted = models.CharField(max_length=200)
    recommended_offset_days = models.IntegerField(
        help_text="Days from birth when this vaccine should be given (e.g., Birth = 0, 6 weeks = 42)")
    dosage_number = models.IntegerField(default=1, help_text="Dose number in the series (e.g., 1, 2, 3)")

    def __str__(self):
        return f"{self.name} (Dose {self.dosage_number}) - Day {self.recommended_offset_days}"


class VaccinationRecord(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ADMINISTERED', 'Administered'),
        ('DELAYED', 'Delayed/Skipped'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.ForeignKey(VaccineDefinition, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    # Dates calculations
    scheduled_date = models.DateField(help_text="Calculated date: DOB + Vaccine Offset")
    actual_administered_date = models.DateField(blank=True, null=True, help_text="The actual day the shot was given")

    administered_by = models.CharField(max_length=150, blank=True, null=True, help_text="Doctor or Nurse name")
    batch_number = models.CharField(max_length=50, blank=True, null=True,
                                    help_text="Vaccine vial batch code for safety tracking")

    class Meta:
        ordering = ['scheduled_date']
        unique_together = ('patient', 'vaccine')  # Prevents duplicate assignments of the same dose

    def __str__(self):
        return f"{self.patient.first_name} - {self.vaccine.name} ({self.status})"