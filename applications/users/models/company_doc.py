from django.db import models

# local
from applications.utils.models import TimeStampModel
from applications.users.models import Company

def company_doc_path(instance, filename):
    return 'docs/companies/{0}/docs/{1}'.format(instance.company_id.name, filename)

class CompanyDoc(TimeStampModel):
    company_id  = models.ForeignKey( Company, on_delete = models.PROTECT )
    name        = models.CharField( "name", max_length = 100 )
    document    = models.FileField( upload_to = company_doc_path, null = True, verbose_name = 'documnent' ) 
    state       = models.BooleanField( "state", default = True )
    
    class Meta:
        db_table = 'CompanyDoc'
        verbose_name = 'company doc'
        verbose_name_plural = 'company docs'
