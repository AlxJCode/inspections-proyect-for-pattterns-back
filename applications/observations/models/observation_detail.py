from django.db import models
from applications.utils.models import TimeStampModel
from applications.observations.models import Observation, ObservationAssessment

STATES = (
    ('0', 'disabled'),
    ('1', 'enabled'),
)


class ObservationDetail ( TimeStampModel ): 
    observation_id                  = models.ForeignKey( Observation, on_delete = models.PROTECT )
    classifier                      = models.CharField( 'classifier', max_length = 100 )
    action_consequence_description  = models.CharField( 'action consequence description', max_length = 150 )
    impact_details                  = models.CharField( 'impact details', max_length = 150 )
    type                            = models.CharField( 'type', max_length = 150 )
    amb_id                          = models.ForeignKey( ObservationAssessment, on_delete = models.PROTECT )
    corrective_tasks                = models.CharField( 'corrective tasks', max_length = 150 )
    cumpliance_date                 = models.DateTimeField( 'cumpliance date' )
    percentage                      = models.IntegerField( 'percentage' )
    observations                    = models.CharField( 'observations', max_length = 150 , null = True, blank = True )
    state                           = models.CharField( 'state', max_length = 50, choices = STATES, default = STATES[1][0] )

    class Meta:
        db_table = 'ObservationDetail'
        verbose_name = 'observation detail'
        verbose_name_plural = 'observation details'