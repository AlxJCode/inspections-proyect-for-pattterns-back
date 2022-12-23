
from django.db import models
from applications.utils.models import TimeStampModel


class History(TimeStampModel):
    table_name  = models.CharField("Nombre Tabla",max_length=50)
    action      = models.CharField("Accion",default="CREATE",max_length=10) # CREATE, DELETE, UPDATE
    table_id    = models.IntegerField("Id Tabla")
    table_value = models.CharField(max_length=500)
    state       = models.BooleanField( "Estado", default = True)

    class Meta:
        db_table = 'history'
        ordering = ["id"]
        verbose_name_plural = "Historiales"
        verbose_name = "Historial"