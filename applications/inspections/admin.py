from django.contrib import admin

# Register your models here.
from applications.inspections.models import *

admin.site.register( Inspection )
admin.site.register( InspectionDetail )
admin.site.register( InspectionDetailEvidence )
admin.site.register( InspectionAffected )
admin.site.register( InspectionAssessment )
admin.site.register( InspectionUser )
admin.site.register( InspectionType )
admin.site.register( InspectionDetailResponsible )