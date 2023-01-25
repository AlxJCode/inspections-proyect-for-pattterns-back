from django.db import models

from applications.utils.models import TimeStampModel
from applications.users.models import SystemUser, Area, Company
from applications.observations.models import ObservationType

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
    user_id                         = models.ForeignKey( SystemUser, on_delete = models.PROTECT )
    user_fullname                   = models.CharField( 'user fullname', max_length = 150 )
    user_dni                        = models.CharField( 'user dni', max_length = 15 )
    user_occupation                 = models.CharField( 'user occupation', max_length = 60, blank = True, null = True )
    user_signature                  = models.FileField( 'user signature', upload_to = user_signature_path, null = True, blank = True )
    area_id                         = models.ForeignKey( Area, on_delete = models.PROTECT, null = True, blank = True )
    area_name                       = models.CharField( 'area name', max_length = 50, default = "" )
    zone_name                       = models.CharField( 'zone name', max_length = 50, default = "" )
    company_id                      = models.ForeignKey( Company, on_delete = models.PROTECT, null = True, blank = True )
    company_name                    = models.CharField( 'company name', max_length = 100 )
    company_ruc                     = models.CharField( 'company ruc', max_length = 30, null = True, blank = True )
    company_activity                = models.CharField( 'company activity', max_length = 60, null = True, blank = True )
    company_address                 = models.CharField( 'company address', max_length = 80, null = True, blank = True )
    company_total_employees         = models.IntegerField( "company total employees", null = True, blank = True )
    observation_objetive            = models.CharField( 'observation objetive', max_length = 100, null = True, blank = True )
    task_name                       = models.CharField( 'task name', max_length = 150 )
    pet_code                        = models.CharField( 'pet code', max_length = 100 )
    guard                           = models.CharField( 'guard', max_length = 32 )
    datetime                        = models.DateTimeField( 'datetime' )
    type_id                         = models.ForeignKey( ObservationType, on_delete = models.PROTECT, null = True, blank = True )
    type                            = models.CharField( 'type', max_length = 50 )
    causes_of_infavourable_results  = models.CharField( "causes of infavourable results", max_length = 100, null = True, blank = True )
    conclutions                     = models.CharField( "conclutions", max_length = 100, null = True, blank = True )
    recommendations                 = models.CharField( 'recommendations', max_length = 100, null = True, blank = True )
    observations                    = models.CharField( 'observations', max_length = 150, blank = True, null = True )
    state                           = models.CharField( 'state', max_length = 50, choices = STATES, default = STATES[0][0] )

    class Meta:
        db_table = 'Observation'
        verbose_name = 'observations'
        verbose_name_plural = 'observation'