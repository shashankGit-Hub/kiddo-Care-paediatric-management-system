from rest_framework import viewsets
from apps.patients.serializers import PatientSerializer
from django.shortcuts import render, get_object_or_404
from apps.patients.models import Patient
from django.shortcuts import render
from django.db.models import Q


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer


def patient_dashboard_view(request, patient_id):
    """
    Renders the unified comprehensive clinical workspace template
    for a single pediatric profile.
    """
    patient = get_object_or_404(Patient, pk=patient_id)

    # We fetch related records efficiently using the related_name properties defined in models
    visits = patient.visits.all().order_by('visit_date')
    vaccinations = patient.vaccinations.all().order_by('scheduled_date')

    context = {
        'patient': patient,
        'visits': visits,
        'vaccinations': vaccinations,
    }
    return render(request, 'patients/dashboard.html', context)


def patient_list_view(request):
    """
    Renders a searchable, filterable master directory of all pediatric profiles.
    """
    # Fetch all records initially
    queryset = Patient.objects.all().order_by('-created_at')

    # Extract structural URL parameters
    search_query = request.GET.get('search', '').strip()
    gender_filter = request.GET.get('gender', '').strip()
    preterm_filter = request.GET.get('is_preterm', '').strip()

    # Apply database conditional filters based on inputs
    if search_query:
        queryset = queryset.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(guardian_name__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )

    if gender_filter:
        queryset = queryset.filter(gender=gender_filter)

    if preterm_filter:
        # Convert string values from query parameters to matching booleans
        is_preterm_bool = preterm_filter.lower() == 'true'
        queryset = queryset.filter(is_preterm=is_preterm_bool)

    context = {
        'patients': queryset,
        'search_query': search_query,
        'gender_filter': gender_filter,
        'preterm_filter': preterm_filter,
    }
    return render(request, 'patients/index.html', context)