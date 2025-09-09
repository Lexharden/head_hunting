from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile for additional information"""
    USER_TYPES = [
        ('job_seeker', 'Buscador de empleo'),
        ('employer', 'Empleador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name="Tipo de usuario")
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    location = models.CharField(max_length=200, verbose_name="Ubicación", blank=True)
    bio = models.TextField(verbose_name="Biografía", blank=True, max_length=500)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="CV")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="Foto de perfil")
    skills = models.TextField(verbose_name="Habilidades", blank=True, help_text="Separar con comas")
    experience_years = models.IntegerField(verbose_name="Años de experiencia", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_user_type_display()}"
