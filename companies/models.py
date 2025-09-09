from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    """Model for companies that post jobs"""
    name = models.CharField(max_length=200, verbose_name="Nombre de la empresa")
    description = models.TextField(verbose_name="Descripción", blank=True)
    website = models.URLField(verbose_name="Sitio web", blank=True)
    location = models.CharField(max_length=200, verbose_name="Ubicación")
    size = models.CharField(max_length=50, verbose_name="Tamaño", choices=[
        ('1-10', '1-10 empleados'),
        ('11-50', '11-50 empleados'),
        ('51-200', '51-200 empleados'),
        ('201-500', '201-500 empleados'),
        ('500+', 'Más de 500 empleados'),
    ], default='1-10')
    industry = models.CharField(max_length=100, verbose_name="Industria", blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Logo")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
