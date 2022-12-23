from django.db import models

from applications.utils.models import TimeStampModel

class InspectionType(TimeStampModel):
    name    = models.CharField( 'name', max_length = 64 )
    subtype = models.CharField( 'subtype', max_length = 100 )

    class Meta:
        db_table = 'InspectionType'
        verbose_name = 'inspection type'
        verbose_name_plural = 'inspection types'