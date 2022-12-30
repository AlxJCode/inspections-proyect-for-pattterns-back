from django.db import models

# local
from applications.utils.models import TimeStampModel
from applications.users.models import SystemUser, Area, Company
from applications.inspections.models import InspectionType

def user_signature_path(instance, filename):
    return 'inpections/signatures/{0}/{1}'.format(instance.user_dni, filename)

STATES = (
    ('0', 'disabled'),
    ('1', 'enabled'),
)

class Inspection(TimeStampModel):
    user_id                         = models.ForeignKey( SystemUser, on_delete = models.PROTECT, related_name = "inspection_user" )
    user_fullname                   = models.CharField( "user fullname", max_length = 150 )
    user_dni                        = models.CharField( "user dni", max_length = 15 )
    user_occupation                 = models.CharField( "user occupation", max_length = 80 , blank = True, null = True )
    user_signature                  = models.FileField( upload_to = user_signature_path, null = True, blank = True, verbose_name= "signature" )
    area_id                         = models.ForeignKey( Area, on_delete = models.PROTECT, null = True, blank = True, related_name = "inspection_area" )
    area_name                       = models.CharField( "area name", max_length = 50 )
    zone_name                       = models.CharField( "zone name", max_length = 60 )
    company_id                      = models.ForeignKey( Company, on_delete = models.PROTECT, null = True, blank = True, related_name = "inspection_company" )
    company_name                    = models.CharField( "company name", max_length = 100 )
    company_address                 = models.CharField( "company address", max_length = 100, null = True, blank = True )
    company_ruc                     = models.CharField( "company ruc", max_length = 20 )
    company_total_employees         = models.IntegerField( "company total employees", null = True, blank = True )
    area_responsible_id             = models.ForeignKey( SystemUser, on_delete = models.PROTECT, null = True, blank = True, related_name = "inspection_area_responsible" )
    area_responsible_fullname       = models.CharField( 'area responsible name', max_length = 150 )
    area_responsible_dni            = models.CharField( 'area responsible dni', max_length = 15 )
    datetime                        = models.DateTimeField( "datetime" )
    type                            = models.ForeignKey( InspectionType, on_delete = models.PROTECT, related_name = "inspection_type" )
    causes_of_infavourable_results  = models.CharField( "causes of infavourable results", max_length = 100, null = True, blank = True )
    conclutions                     = models.CharField( "conclutions", max_length = 100, null = True, blank = True )
    recommendations                 = models.CharField( 'recommendations', max_length = 100, null = True, blank = True )
    observations                    = models.CharField( 'observations', max_length = 100, null = True, blank = True )
    state                           = models.CharField( 'state', max_length = 100, choices = STATES, default = STATES[1][0] ) 

    class Meta:
        db_table = 'Inspection'
        verbose_name = 'inspection'
        verbose_name_plural = 'inspections'
