from django.db import models
from applications.utils.models import TimeStampModel
from applications.observations.models import Observation, ObservationAssessment, ObservationAffected

STATES = (
    ('0', 'disabled'),
    ('1', 'enabled'),
)


class ObservationDetail ( TimeStampModel ): 
    observation_id                  = models.ForeignKey( Observation, on_delete = models.PROTECT, related_name = "observation_detail" )
    affected_id                     = models.ForeignKey( ObservationAffected, on_delete = models.PROTECT, null = True, blank = True, related_name = "observation_detail_affected" )
    affected_code                   = models.CharField( 'affected code', max_length = 100, null = True, blank = True )
    affected_name                   = models.CharField( 'affected name', max_length = 100, null = True, blank = True )
    action_consequence_description  = models.CharField( 'action consequence description', max_length = 150 )
    impact_details                  = models.CharField( 'impact details', max_length = 150 )
    type                            = models.CharField( 'type', max_length = 150 )
    assesment_id                    = models.ForeignKey( ObservationAssessment, on_delete = models.PROTECT, related_name = "observation_detail_assesment" )
    assesment_name                  = models.CharField( 'assesment name', max_length = 100, null = True, blank = True )
    corrective_tasks                = models.CharField( 'corrective tasks', max_length = 150 )
    compliance_date                 = models.DateTimeField( 'compliance date', null = True, blank = True )
    percentage                      = models.IntegerField( 'percentage', default = 0 )
    observations                    = models.CharField( 'observations', max_length = 150 , null = True, blank = True )
    state                           = models.CharField( 'state', max_length = 50, choices = STATES, default = STATES[1][0] )

    class Meta:
        db_table = 'ObservationDetail'
        verbose_name = 'observation detail'
        verbose_name_plural = 'observation details'