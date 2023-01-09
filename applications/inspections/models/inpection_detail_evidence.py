from django.db import models

from applications.utils.models import TimeStampModel
from applications.inspections.models import InspectionDetail

def inspection_detail_evidence_path(instance, filename):
    return 'inpections/details/{0}/{1}'.format(instance.inspection_detail_id.id, filename)

TYPES = (
    ('0', 'Init'),
    ('1', "Correct")
)

class InspectionDetailEvidence(TimeStampModel):
    inspection_detail_id= models.ForeignKey( InspectionDetail, on_delete = models.PROTECT, verbose_name = "inspection_detail_evidence" )
    evidence            = models.FileField( upload_to = inspection_detail_evidence_path )
    percentage          = models.IntegerField( 'percentage' )
    type                = models.CharField( 'type', max_length = 50, choices = TYPES )
    state               = models.BooleanField( 'state', default = True )

    class Meta:
        db_table = 'InspectionDetailEvidence'
        verbose_name = 'inspection detail evidence'
        verbose_name_plural = 'inspection detail evidences'