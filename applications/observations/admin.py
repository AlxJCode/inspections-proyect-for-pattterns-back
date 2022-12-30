from django.contrib import admin
from applications.observations.models import *

# Register your models here.

admin.site.register( Observation )
admin.site.register( ObservationUser )
admin.site.register( ObservationResponsible )
admin.site.register( ObservationQuestion )
admin.site.register( ObservationEvidence )
admin.site.register( ObservationDetail )
admin.site.register( ObservationAssessment )
admin.site.register( ObservationAnswer )