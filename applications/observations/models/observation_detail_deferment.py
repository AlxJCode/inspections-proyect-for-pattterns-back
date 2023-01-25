from django.db import models

from applications.utils.models import TimeStampModel
from applications.observations.models import ObservationDetail
from applications.users.models import SystemUser

class ObservationDetailDeferment( TimeStampModel ):
    observation_detail_id   = models.ForeignKey( ObservationDetail, on_delete = models.PROTECT )
    user_id                 = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True )
    cumpliance_date         = models.DateTimeField( 'cumpliance date' )
    observations            = models.CharField( 'observations', max_length = 124, null = True, blank = True )
    state                   = models.BooleanField( 'state', default = True )

    class Meta:
        db_table = 'ObservationDetailDeferment'
        verbose_name = 'observation detail deferment'
        verbose_name_plural = 'observation detail deferments'
    