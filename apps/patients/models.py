from django.db import models


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A Positive'), ('A-', 'A Negative'),
        ('B+', 'B Positive'), ('B-', 'B Negative'),
        ('AB+', 'AB Positive'), ('AB-', 'AB Negative'),
        ('O+', 'O Positive'), ('O-', 'O Negative'),
        ('UNK', 'Unknown'),
    ]

    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default='UNK')

    # Guardian Info
    guardian_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    # Medical History Context
    chronic_conditions = models.TextField(blank=True, null=True, help_text="E.g., Asthma, Type 1 Diabetes")
    allergies = models.TextField(blank=True, null=True, help_text="Food, drug, or environmental allergies")
    is_preterm = models.BooleanField(default=False, help_text="Was the child born preterm?")
    birth_weight_kg = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True,
                                          help_text="Birth weight in kilograms (e.g., 3.250)")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"