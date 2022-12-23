from django.db import models

from applications.utils.models import TimeStampModel
from applications.users.models import SystemUser, Area, Company

def user_signature_path(instance, filename):
    return 'observations/signatures/{0}/{1}'.format(instance.user_dni, filename)

STATES = (
    ('0', 'disabled'),
    ('1', 'enabled'),
)

TYPES = (
    ('0', 'not planified'),
    ('1', 'planified'),
)

class Observation( TimeStampModel ):
    user_id         = models.ForeignKey( SystemUser, on_delete = models.PROTECT )
    user_fullname   = models.CharField( 'user fullname', max_length = 150 )
    user_dni        = models.CharField( 'user dni', max_length = 15 )
    user_signature  = models.FileField( 'user signature', upload_to = user_signature_path, null = True, blank = True )
    area_id         = models.ForeignKey( Area, on_delete = models.PROTECT, null = True, blank = True )
    area_name       = models.CharField( 'area name', max_length = 50 )
    company_id      = models.ForeignKey( Company, on_delete = models.PROTECT, null = True, blank = True )
    company_name    = models.CharField( 'company name', max_length = 100 )
    company_ruc     = models.CharField( 'company ruc', max_length = 30, null = True, blank = True )
    task_name       = models.CharField( 'task name', max_length = 150 )
    pet_code        = models.CharField( 'pet code', max_length = 100 )
    guard           = models.CharField( 'guard', max_length = 32 )
    datetime        = models.DateTimeField( 'datetime' )
    type            = models.CharField( 'type', max_length = 50, choices = TYPES )
    observations    = models.CharField( 'observations', max_length = 150, blank = True, null = True )
    state           = models.CharField( 'state', max_length = 50, choices = STATES, default = STATES[0][0] )

    class Meta:
        db_table = 'Observation'
        verbose_name = 'observations'
        verbose_name_plural = 'observation'