from django.db import models
from applications.observations.models import Observation, ObservationQuestion
from applications.utils.models import TimeStampModel


class ObservationAnswer( TimeStampModel ):
    observation_id  = models.ForeignKey( Observation, on_delete = models.PROTECT )
    question_id     = models.ForeignKey( ObservationQuestion, on_delete = models.PROTECT )
    response        = models.CharField ( 'response', max_length = 150 )

    class Meta:
        db_table = 'ObservationAnswer'
        verbose_name = 'observation answer'
        verbose_name_plural = 'observation answers'
