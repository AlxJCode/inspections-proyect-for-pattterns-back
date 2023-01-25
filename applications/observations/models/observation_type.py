from django.db import models
from applications.utils.models import TimeStampModel

class ObservationType ( TimeStampModel ):
    type        = models.CharField( 'type', max_length = 80 )
    subtype     = models.CharField ( 'subtype', max_length = 80 )

    class Meta:
        db_table = 'ObservationType'
        verbose_name = 'observation type'
        verbose_name_plural = 'observation types'