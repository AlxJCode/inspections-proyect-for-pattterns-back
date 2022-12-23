from django.db import models

from applications.utils.models import TimeStampModel

class InspectionAffected( TimeStampModel ):
    name    = models.CharField( 'name', max_length = 150 )
    state   = models.BooleanField( 'state', default = True ) 

    class Meta:
        db_table = 'InspectionAffected'
        verbose_name = 'inspection affected'
        verbose_name_plural = 'inspection affected'