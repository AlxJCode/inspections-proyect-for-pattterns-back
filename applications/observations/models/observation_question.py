from django.db import models
from applications.utils.models import TimeStampModel

class ObservationQuestion ( TimeStampModel ):
    code        = models.CharField( 'code', max_length = 100 )
    order       = models.IntegerField ( 'order' )
    question    = models.CharField( 'question', max_length = 255 )

    class Meta:
        db_table = 'ObservationQuestion'
        verbose_name = 'observation question'
        verbose_name_plural = 'observation questions'