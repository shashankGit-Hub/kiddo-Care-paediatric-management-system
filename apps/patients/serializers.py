from rest_framework import serializers
from apps.patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    # Dynamically compute a human-readable display string for age
    age_display = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'blood_type', 'age_display', 'guardian_name', 'contact_number',
            'email', 'address', 'chronic_conditions', 'allergies',
            'is_preterm', 'birth_weight_kg', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_age_display(self, obj):
        """Calculates child's current age in years and months dynamically."""
        from datetime import date
        today = date.today()
        dob = obj.date_of_birth

        years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Calculate remaining months
        if today.month >= dob.month:
            months = today.month - dob.month
        else:
            months = 12 + today.month - dob.month

        if today.day < dob.day:
            months -= 1
            if months < 0:
                months = 11
                years -= 1

        if years == 0:
            return f"{months} Months"
        return f"{years} Years, {months} Months"