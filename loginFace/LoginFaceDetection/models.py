from tabnanny import verbose
from django.db import models

# Create your models here.

class users(models.Model):
    usuario= models.CharField(max_length=30, null=False, verbose_name='Usuario')
    password = models.CharField(max_length=10,null=False, verbose_name='Contrasena')
    foto = models.ImageField(upload_to='img', blank=True)
