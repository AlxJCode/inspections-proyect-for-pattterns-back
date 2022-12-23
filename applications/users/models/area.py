from django.db import models

# local
from applications.utils.models import TimeStampModel
from applications.users.models import Company

class Area(TimeStampModel):
    company_id  = models.ForeignKey( Company, on_delete = models.PROTECT )
    name        = models.CharField( "name", max_length = 100 )
    state       = models.BooleanField( "state", default = True )

    class Meta:
        db_table = 'Area'
        verbose_name = 'area'
        verbose_name_plural = 'areas'
