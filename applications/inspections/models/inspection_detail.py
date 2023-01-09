from django.db import models

from applications.utils.models import TimeStampModel
from applications.inspections.models import Inspection, InspectionAffected, InspectionAssessment

STATES = (
    ('0', 'Pending'),
    ('1', 'Refused'),
)

class InspectionDetail(TimeStampModel):
    inspection_id                   = models.ForeignKey( Inspection, on_delete = models.PROTECT, related_name = "inspection_detail" )
    affected_id                     = models.ForeignKey( InspectionAffected, on_delete = models.PROTECT, related_name = "inspection_detail_affected" )
    affected_name                   = models.CharField ( 'affected name', max_length = 100 )
    site                            = models.CharField( 'site', max_length = 50 )
    action_consequence_description  = models.CharField( 'action consequence description', max_length = 150 )
    impact_details                  = models.CharField ( 'impact details', max_length = 150 ) 
    type                            = models.CharField ( 'type', max_length = 50 )
    assesment_id                    = models.ForeignKey( InspectionAssessment, on_delete = models.PROTECT, related_name = "inspection_detail_assesment" )
    assesment_name                  = models.CharField ( 'assesment name', max_length = 100 )
    assesment_code                  = models.CharField ( 'assesment code', max_length = 100 )
    corrective_tasks                = models.CharField( 'corrective tasks', max_length = 100 )
    compliance_date                 = models.DateTimeField( 'compliance date' )
    percentage                      = models.IntegerField( 'percentage' )
    observations                    = models.CharField( 'observations', max_length = 100, null = True, blank = True )
    state                           = models.CharField( 'state', max_length = 50, choices = STATES, default = STATES[0][0] )

    class Meta:
        db_table = 'InspectionDetail'
        verbose_name = 'inspections detail'
        verbose_name_plural = 'inspections details'
