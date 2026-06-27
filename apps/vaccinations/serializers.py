from rest_framework import serializers
from apps.vaccinations.models import VaccinationRecord, VaccineDefinition

class VaccineDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineDefinition
        fields = '__all__'

class VaccinationRecordSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.ReadOnlyField(source='vaccine.name')
    disease_targeted = serializers.ReadOnlyField(source='vaccine.disease_targeted')

    class Meta:
        model = VaccinationRecord
        fields = [
            'id', 'patient', 'vaccine', 'vaccine_name', 'disease_targeted',
            'status', 'scheduled_date', 'actual_administered_date',
            'administered_by', 'batch_number'
        ]
