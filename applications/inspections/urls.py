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
    path('inpection-users/', InspectionUserListView.as_view()),
    path('inpection-users/<int:pk>/', InspectionUserDetailView.as_view()),
    path('inpection-users/filters/', InspectionUserFiltersView.as_view()),

    # Inspection Types 
    path('inpection-types/', InspectionTypeListView.as_view()),
    path('inpection-types/<int:pk>/', InspectionTypeDetailView.as_view()),
    path('inpection-types/filters/', InspectionTypeFiltersView.as_view()),

    # Inspection Details 
    path('inpection-details/', InspectionDetailListView.as_view()),
    path('inpection-details/<int:pk>/', InspectionDetailDetailView.as_view()),
    path('inpection-details/filters/', InspectionDetailFiltersView.as_view()),

    # Inspection Details evidence
    path('inpection-detail-evidences/', InspectionDetailEvidenceListView.as_view()),
    path('inpection-detail-evidences/<int:pk>/', InspectionDetailEvidenceDetailView.as_view()),
    path('inpection-detail-evidences/filters/', InspectionDetailEvidenceFiltersView.as_view()),

    # Inspection Details responsible
    path('inpection-detail-responsibles/', InspectionDetailResponsibleListView.as_view()),
    path('inpection-detail-responsibles/<int:pk>/', InspectionDetailResponsibleDetailView.as_view()),
    path('inpection-detail-responsibles/filters/', InspectionDetailResponsibleFiltersView.as_view()),

    # Inspection Affected
    path('inpection-affected/', InspectionAffectedListView.as_view()),
    path('inpection-affected/<int:pk>/', InspectionAffectedDetailView.as_view()),
    path('inpection-affected/filters/', InspectionAffectedFiltersView.as_view()),

    # Inspection Assessment
    path('inpection-assessments/', InspectionAssessmentListView.as_view()),
    path('inpection-assessments/<int:pk>/', InspectionAssessmentDetailView.as_view()),
    path('inpection-assessments/filters/', InspectionAssessmentFiltersView.as_view()),

]