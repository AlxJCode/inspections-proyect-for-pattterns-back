from django.db import models
from django.contrib.auth.models import User
from applications.users.models import Area
from applications.utils.models import TimeStampModel

U = "U"
USER_TYPES = (
    (U, "User"),
    ('INS', "Inspector"),
    ('SUP', "Supervisor"),
    ('SA', "Super administrador"),
)

class SystemUser(TimeStampModel):

    auth_user           = models.OneToOneField( User, on_delete = models.DO_NOTHING, db_column = 'auth_user_id', blank = False, null = False )
    name                = models.CharField( "name", max_length = 60 )
    first_last_name     = models.CharField( "first lastname", max_length = 50 )
    second_last_name    = models.CharField( "second lastname", max_length = 50 )
    position            = models.CharField('position', max_length = 100, blank = True, null = True )
    email               = models.EmailField( "email", max_length = 100, null = True, blank = True )
    type                = models.CharField( "type", max_length = 50, choices = USER_TYPES, default = U )
    phone               = models.CharField( "phone", max_length = 15, null = True, blank = True )
    area_id             = models.ForeignKey( Area, on_delete = models.PROTECT, blank = True, null = True )
    dni                 = models.CharField( "dni", max_length = 20, unique = True )
    state               = models.BooleanField( "state", default = True )

    class Meta:
        db_table = 'SystemUser'
        verbose_name = 'system user'
        verbose_name_plural = 'system users'
    
    def __str__(self):
        return str( self.id ) + " " + self.name + " " + self.dni
