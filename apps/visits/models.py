from django.db import models
from apps.patients.models import Patient


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(auto_now_add=True)

    # Highly exact decimal definitions for pediatric plotting
    weight_kg = models.DecimalField(max_digits=5, decimal_places=3, help_text="Weight in kg (e.g., 12.450)")
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height/Length in cm (e.g., 85.50)")
    head_circumference_cm = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,
                                                help_text="Head circumference in cm")

    clinical_notes = models.TextField(blank=True, null=True, help_text="Doctor's observations, symptoms, diagnosis")

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"Visit for {self.patient.first_name} on {self.visit_date.strftime('%Y-%m-%d')}"

    @property
    def age_at_visit_months(self):
        """Calculates precise age in months at the exact moment of this specific check-up."""
        delta = self.visit_date.date() - self.patient.date_of_birth
        return round(delta.days / 30.4375, 2)  # Average days in a month