from django.db import models

# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Carpeta"
        verbose_name_plural = "Carpetas"
