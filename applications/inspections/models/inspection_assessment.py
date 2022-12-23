from django.db import models

from applications.utils.models import TimeStampModel

class InspectionAssessment( TimeStampModel ):
    gravity     = models.CharField( 'gravity', max_length = 50 )
    state       = models.BooleanField( 'state', default = True ) 

    class Meta:
        db_table = 'InspectionAssessment'
        verbose_name = 'inspection assessment'
        verbose_name_plural = 'inspection assessments'