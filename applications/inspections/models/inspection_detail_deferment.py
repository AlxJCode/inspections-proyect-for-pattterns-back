from django.db import models

from applications.utils.models import TimeStampModel
from applications.inspections.models import InspectionDetail
from applications.users.models import SystemUser

class InspectionDetailDeferment( TimeStampModel ):
    inspection_detail_id = models.ForeignKey( InspectionDetail, on_delete = models.PROTECT )
    user_id             = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True )
    cumpliance_date     = models.DateTimeField( 'cumpliance date' )
    observations        = models.CharField( 'observations', max_length = 124, null = True, blank = True )
    state               = models.BooleanField( 'state', default = True )

    class Meta:
        db_table = 'InspectionDetailDeferment'
        verbose_name = 'inspection detail deferment'
        verbose_name_plural = 'inspection detail deferments'
    