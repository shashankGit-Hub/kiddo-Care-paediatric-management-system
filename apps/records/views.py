from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.patients.models import Patient
from apps.visits.models import Visit
from apps.records.utils import calculate_growth_analytics


class PatientGrowthAnalyticsView(APIView):
    """
    API endpoint that aggregates and delivers historical physical metrics
    for real-time charting interfaces.
    """

    def get(self, request, patient_id, format=None):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Pull all recorded biological encounters
        visits = Visit.objects.filter(patient=patient)

        # Parse data streams via utility matrix
        chart_payload = calculate_growth_analytics(visits)

        # Append target metadata context
        chart_payload['patient_name'] = f"{patient.first_name} {patient.last_name}"
        chart_payload['gender'] = patient.gender

        return Response(chart_payload, status=status.HTTP_200_OK)