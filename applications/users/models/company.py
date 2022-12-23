from django.db import models

# local
from applications.utils.models import TimeStampModel

class Company(TimeStampModel):
    name                = models.CharField( "name", max_length = 100 )
    ruc                 = models.CharField( "ruc", max_length = 50  )
    economic_activity   = models.CharField( 'economic activity', max_length = 100 )
    address             = models.CharField( "address", max_length = 150, null = True, blank = True )
    state               = models.BooleanField( "state", default = True )

    class Meta:
        db_table = 'Company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'
