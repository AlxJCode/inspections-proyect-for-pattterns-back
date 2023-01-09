from django.urls import path

from applications.inspections.api_views.inspection_views import *
from applications.inspections.api_views.inspection_affected_views import *
from applications.inspections.api_views.inspection_assessment_views import *
from applications.inspections.api_views.inspection_detail_evidence_views import *
from applications.inspections.api_views.inspection_user_views import *
from applications.inspections.api_views.inspection_type_views import *
from applications.inspections.api_views.inspection_detail_respnsible_views import *
from applications.inspections.api_views.inspection_detail_views import *

urlpatterns = [

    # Inspections
    path('inspections/', InspectionListView.as_view()),
    path('inspections/<int:pk>/', InspectionDetailView.as_view()),
    path('inspections/filters/', InspectionFiltersView.as_view()),

    # Inspection Users 
    path('inspection-users/', InspectionUserListView.as_view()),
    path('inspection-users/<int:pk>/', InspectionUserDetailView.as_view()),
    path('inspection-users/filters/', InspectionUserFiltersView.as_view()),

    # Inspection Types 
    path('inspection-types/', InspectionTypeListView.as_view()),
    path('inspection-types/<int:pk>/', InspectionTypeDetailView.as_view()),
    path('inspection-types/filters/', InspectionTypeFiltersView.as_view()),

    # Inspection Details 
    path('inspection-details/', InspectionDetailListView.as_view()),
    path('inspection-details/<int:pk>/', InspectionDetailDetailView.as_view()),
    path('inspection-details/filters/', InspectionDetailFiltersView.as_view()),

    # Inspection Details evidence
    path('inspection-detail-evidences/', InspectionDetailEvidenceListView.as_view()),
    path('inspection-detail-evidences/<int:pk>/', InspectionDetailEvidenceDetailView.as_view()),
    path('inspection-detail-evidences/filters/', InspectionDetailEvidenceFiltersView.as_view()),

    # Inspection Details responsible
    path('inspection-detail-responsibles/', InspectionDetailResponsibleListView.as_view()),
    path('inspection-detail-responsibles/<int:pk>/', InspectionDetailResponsibleDetailView.as_view()),
    path('inspection-detail-responsibles/filters/', InspectionDetailResponsibleFiltersView.as_view()),

    # Inspection Affected
    path('inspection-affected/', InspectionAffectedListView.as_view()),
    path('inspection-affected/<int:pk>/', InspectionAffectedDetailView.as_view()),
    path('inspection-affected/filters/', InspectionAffectedFiltersView.as_view()),

    # Inspection Assessment
    path('inspection-assessments/', InspectionAssessmentListView.as_view()),
    path('inspection-assessments/<int:pk>/', InspectionAssessmentDetailView.as_view()),
    path('inspection-assessments/filters/', InspectionAssessmentFiltersView.as_view()),

]