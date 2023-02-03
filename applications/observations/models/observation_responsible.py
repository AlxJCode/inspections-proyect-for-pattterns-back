from django.db import models

from applications.utils.models import TimeStampModel
from applications.observations.models import ObservationDetail
from applications.users.models import SystemUser

class ObservationResponsible( TimeStampModel ):
    user_id                 = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True )
    observation_detail_id   = models.ForeignKey( ObservationDetail, on_delete = models.PROTECT, related_name = "odr" )
    user_fullname           = models.CharField( 'user fullname', max_length = 150 )
    user_dni                = models.CharField( 'user dni', max_length = 15 )
    user_phone              = models.CharField( 'user phone', max_length = 15, null = True, blank = True )
    user_email              = models.EmailField( 'user email', max_length = 64, null = True, blank = True )

    class Meta:
        db_table = 'ObservationResponsible'
        verbose_name = 'observation responsible'
        verbose_name_plural = 'observation responsibles'