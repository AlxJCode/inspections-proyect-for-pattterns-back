from django.db import models

from applications.utils.models import TimeStampModel
from applications.users.models import SystemUser
from applications.inspections.models import Inspection

TYPES = (
    ('0', 'Inspector'),
    ('1', 'Inspected'),
)

class InspectionUser(TimeStampModel):
    user_id         = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True )
    inspection_id   = models.ForeignKey( Inspection, on_delete = models.PROTECT )
    type            = models.CharField( 'type', max_length = 50, choices = TYPES )
    dni             = models.CharField( 'dni', max_length = 15 )
    user_fullname   = models.CharField( 'user_fullname', max_length = 150 )
    occupation      = models.CharField( 'occupation', max_length = 100, null = True, blank = True )
    experience      = models.CharField( 'experience', max_length = 100, null = True, blank = True )

    class Meta:
        db_table = 'InspectionUser'
        verbose_name = 'inspection user'
        verbose_name_plural = 'inspection users'