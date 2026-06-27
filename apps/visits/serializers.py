from rest_framework import serializers
from apps.visits.models import Visit

class VisitSerializer(serializers.ModelSerializer):
    # Pull in calculated property from the model layer
    age_at_visit = serializers.ReadOnlyField(source='age_at_visit_months')

    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'visit_date', 'weight_kg',
            'height_cm', 'head_circumference_cm',
            'clinical_notes', 'age_at_visit'
        ]
        read_only_fields = ['id', 'visit_date', 'age_at_visit']