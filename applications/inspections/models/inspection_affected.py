from django.db import models

from applications.utils.models import TimeStampModel

class InspectionAffected( TimeStampModel ):
    name    = models.CharField( 'name', max_length = 150 )
    code    = models.CharField( 'code', max_length = 120, null = True, blank = True )
    state   = models.BooleanField( 'state', default = True ) 

    class Meta:
        db_table = 'InspectionAffected'
        verbose_name = 'inspection affected'
        verbose_name_plural = 'inspection affected'