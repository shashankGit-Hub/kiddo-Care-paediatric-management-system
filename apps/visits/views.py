from rest_framework import viewsets
from apps.visits.models import Visit
from apps.visits.serializers import VisitSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def get_queryset(self):
        """Allows filtering visits down to a specific child via query parameters."""
        queryset = Visit.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
