from rest_framework import viewsets
from apps.vaccinations.models import VaccinationRecord, VaccineDefinition
from apps.vaccinations.serializers import VaccinationRecordSerializer, VaccineDefinitionSerializer


class VaccineDefinitionViewSet(viewsets.ModelViewSet):
    queryset = VaccineDefinition.objects.all()
    serializer_class = VaccineDefinitionSerializer


class VaccinationRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer

    def get_queryset(self):
        """Allows sorting and filtering a specific child's immunization calendar."""
        queryset = VaccinationRecord.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        status = self.request.query_params.get('status')

        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset