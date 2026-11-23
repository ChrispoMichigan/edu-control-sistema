from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(eliminado_en__isnull=True)


class SoftDeleteModel(models.Model):

    eliminado_en = models.DateTimeField(null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    todos = models.Manager()

    class Meta:
        abstract = True

    def eliminar(self):
        self.eliminado_en = timezone.now()
        self.save(update_fields=['eliminado_en'])

    def restaurar(self):
        self.eliminado_en = None
        self.save(update_fields=['eliminado_en'])
