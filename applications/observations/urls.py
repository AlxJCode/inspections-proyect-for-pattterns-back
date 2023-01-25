from django.urls import path

from applications.observations.api_views.observation_views import *
from applications.observations.api_views.observation_answer_views import *
from applications.observations.api_views.observation_assessment_views import *
from applications.observations.api_views.observation_detail_views import *
from applications.observations.api_views.observation_responsible_views import *
from applications.observations.api_views.observation_user_views import *
from applications.observations.api_views.observation_question_views import *
from applications.observations.api_views.observation_evidence_views import *
from applications.observations.api_views.observation_affected_views import *
from applications.observations.api_views.observation_detail_deferment_views import *
from applications.observations.api_views.observation_type_views import *

urlpatterns = [

    # Observations
    path('observations/', ObservationListView.as_view()),
    path('observations/<int:pk>/', ObservationDetailView.as_view()),
    path('observations/filters/', ObservationFiltersView.as_view()),

    # Observation Users 
    path('observation-users/', ObservationUserListView.as_view()),
    path('observation-users/<int:pk>/', ObservationUserDetailView.as_view()),
    path('observation-users/filters/', ObservationUserFiltersView.as_view()),

    # Observation Types 
    path('observation-types/', ObservationTypeListView.as_view()),
    path('observation-types/<int:pk>/', ObservationTypeDetailView.as_view()),
    path('observation-types/filters/', ObservationTypeFiltersView.as_view()),

    # Observation Details 
    path('observation-details/', ObservationDetailListView.as_view()),
    path('observation-details/<int:pk>/', ObservationDetailDetailView.as_view()),
    path('observation-details/filters/', ObservationDetailFiltersView.as_view()),

    # Observation detail Responsible 
    path('observation-detail-responsibles/', ObservationResponsibleListView.as_view()),
    path('observation-detail-responsibles/<int:pk>/', ObservationResponsibleDetailView.as_view()),
    path('observation-detail-responsibles/filters/', ObservationResponsibleFiltersView.as_view()),

    # Observation detail Deferment 
    path('observation-detail-deferments/', ObservationDetailDefermentListView.as_view()),
    path('observation-detail-deferments/<int:pk>/', ObservationDetailDefermentDetailView.as_view()),
    path('observation-detail-deferments/filters/', ObservationDetailDefermentFiltersView.as_view()),

    # Observation Details evidences
    path('observation-detail-evidences/', ObservationEvidenceListView.as_view()),
    path('observation-detail-evidences/<int:pk>/', ObservationEvidenceDetailView.as_view()),
    path('observation-detail-evidences/filters/', ObservationEvidenceFiltersView.as_view()),

    # Observation Details assessments
    path('observation-detail-assessments/', ObservationAssessmentListView.as_view()),
    path('observation-detail-assessments/<int:pk>/', ObservationAssessmentDetailView.as_view()),
    path('observation-detail-assessments/filters/', ObservationAssessmentFiltersView.as_view()),

    # Observation question
    path('observation-questions/', ObservationQuestionListView.as_view()),
    path('observation-questions/<int:pk>/', ObservationQuestionDetailView.as_view()),
    path('observation-questions/filters/', ObservationQuestionFiltersView.as_view()),

    # Observation affected
    path('observation-affecteds/', ObservationAffectedListView.as_view()),
    path('observation-affecteds/<int:pk>/', ObservationAffectedDetailView.as_view()),
    path('observation-affecteds/filters/', ObservationAffectedFiltersView.as_view()),

    # Observation answers
    path('observation-answers/', ObservationAnswerListView.as_view()),
    path('observation-answers/<int:pk>/', ObservationAnswerDetailView.as_view()),
    path('observation-answers/filters/', ObservationAnswerFiltersView.as_view()),

]