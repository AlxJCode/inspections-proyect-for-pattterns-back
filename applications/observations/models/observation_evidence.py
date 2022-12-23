from django.db import models

from applications.utils.models import TimeStampModel
from applications.observations.models import ObservationDetail

def observation_detail_evidence_path(instance, filename):
    return 'observations/details/{0}/{1}'.format(instance.observation_detail_id.id, filename)

TYPES = (
    ('0', 'Init'),
    ('1', "Correct")
)

class ObservationEvidence( TimeStampModel ):
    observation_detail_id   = models.ForeignKey( ObservationDetail, on_delete = models.PROTECT, verbose_name = "observation_detail_evidence" )
    evidence                = models.FileField( 'evidence', upload_to = observation_detail_evidence_path )
    type                    = models.CharField( 'type', max_length = 50 , choices = TYPES )

    class Meta:
        db_table = 'ObservationDetailEvidence'
        verbose_name = 'observation detail evidence'
        verbose_name_plural = 'observation detail evidences'