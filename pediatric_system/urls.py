from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.patients.views import PatientViewSet
from apps.visits.views import VisitViewSet
from apps.vaccinations.views import VaccineDefinitionViewSet, VaccinationRecordViewSet
from apps.records.views import PatientGrowthAnalyticsView
from apps.patients.views import patient_dashboard_view
from apps.patients.views import patient_list_view

# Create an elegant uniform REST routing architecture
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'vaccine-definitions', VaccineDefinitionViewSet, basename='vaccine-definition')
router.register(r'vaccination-records', VaccinationRecordViewSet, basename='vaccination-record')

urlpatterns = [
    path('admin/', admin.site.url_scaffold if hasattr(admin.site, 'url_scaffold') else admin.site.urls),
    path('api/', include(router.urls)), # Exposes endpoints via /api/patients/ and /api/visits/
]

urlpatterns += [
    path('api/patients/<int:patient_id>/growth-analytics/', PatientGrowthAnalyticsView.as_view(), name='patient-growth-analytics'),
]

urlpatterns += [
    path('patients/<int:patient_id>/dashboard/', patient_dashboard_view, name='patient-dashboard'),
]

urlpatterns += [
    path('', patient_list_view, name='patient-list'), # 👈 Root address loads your new index list view
]