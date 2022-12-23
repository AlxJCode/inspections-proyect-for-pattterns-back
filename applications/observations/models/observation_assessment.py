from django.db import models
from applications.utils.models import TimeStampModel

class ObservationAssessment( TimeStampModel ):
    gravity = models.CharField( 'gravity', max_length = 100 )
    state   = models.BooleanField( 'state', default = True )

    class Meta:
        db_table = 'ObservationAssessment'
        verbose_name = 'observation assessment'
        verbose_name_plural = 'observation assessments'