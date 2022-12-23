from django.db import models

from applications.utils.models import TimeStampModel
from applications.inspections.models import InspectionDetail
from applications.users.models import SystemUser

class InspectionDetailResponsible(TimeStampModel):
    inpection_detail_id = models.ForeignKey( InspectionDetail, on_delete = models.PROTECT )
    user_id             = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True )
    user_fullname       = models.CharField( 'user fullname', max_length = 150 )
    user_dni            = models.CharField( 'user dni', max_length = 15 )
    user_phone           = models.CharField( 'user phone', max_length = 15, null = True, blank = True )
    user_email            = models.EmailField( 'user email', max_length = 64, null = True, blank = True )

    class Meta:
        db_table = 'InspectionDetailResponsible'
        verbose_name = 'inspection detail responsible'
        verbose_name_plural = 'inspection detail responsibles'
    