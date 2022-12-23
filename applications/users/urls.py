from django.urls import path

from applications.users.api_views.system_user_views import *
from applications.users.api_views.area_views import *
from applications.users.api_views.company_views import *
from applications.users.api_views.company_doc_views import *

urlpatterns = [

    # System users
    path('users/', SystemUserListView.as_view()),
    path('users/<int:pk>/', SystemUserDetailView.as_view()),
    path('users/filters/', SystemUserFiltersView.as_view()),
    path('users/password/', SystemUserPasswordView.as_view()),

    # Areas 
    path('areas/', AreaListView.as_view()),
    path('areas/<int:pk>/', AreaDetailView.as_view()),
    path('areas/filters/', AreaFiltersView.as_view()),

    # Companies
    path('companies/', CompanyListView.as_view()),
    path('companies/<int:pk>/', CompanyDetailView.as_view()),
    path('companies/filters/', CompanyFiltersView.as_view()),

    # Company Docs
    path('company-docs/', CompanyDocListView.as_view()),
    path('company-docs/<int:pk>/', CompanyDocDetailView.as_view()),
    path('company-docs/filters/', CompanyDocFiltersView.as_view()),

]