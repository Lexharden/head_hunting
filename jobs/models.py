from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

class Job(models.Model):
    """Model for job postings"""
    JOB_TYPES = [
        ('full_time', 'Tiempo completo'),
        ('part_time', 'Tiempo parcial'),
        ('contract', 'Contrato'),
        ('internship', 'Prácticas'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('entry', 'Nivel de entrada'),
        ('junior', 'Junior'),
        ('mid', 'Intermedio'),
        ('senior', 'Senior'),
        ('executive', 'Ejecutivo'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título del puesto")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Empresa")
    description = models.TextField(verbose_name="Descripción del puesto")
    requirements = models.TextField(verbose_name="Requisitos")
    location = models.CharField(max_length=200, verbose_name="Ubicación")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, verbose_name="Tipo de trabajo")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, verbose_name="Nivel de experiencia")
    salary_min = models.PositiveIntegerField(verbose_name="Salario mínimo", null=True, blank=True)
    salary_max = models.PositiveIntegerField(verbose_name="Salario máximo", null=True, blank=True)
    currency = models.CharField(max_length=3, default='EUR', verbose_name="Moneda")
    remote_work = models.BooleanField(default=False, verbose_name="Trabajo remoto")
    skills_required = models.TextField(verbose_name="Habilidades requeridas", blank=True, help_text="Separar con comas")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Publicado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    expires_at = models.DateTimeField(verbose_name="Fecha de expiración", null=True, blank=True)

    class Meta:
        verbose_name = "Oferta de trabajo"
        verbose_name_plural = "Ofertas de trabajo"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    @property
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_min:,} - {self.salary_max:,} {self.currency}"
        elif self.salary_min:
            return f"Desde {self.salary_min:,} {self.currency}"
        elif self.salary_max:
            return f"Hasta {self.salary_max:,} {self.currency}"
        return "Salario a negociar"


class JobApplication(models.Model):
    """Model for job applications"""
    STATUS_CHOICES = [
        ('applied', 'Aplicado'),
        ('reviewing', 'En revisión'),
        ('interview', 'Entrevista'),
        ('rejected', 'Rechazado'),
        ('accepted', 'Aceptado'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name="Oferta de trabajo")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Candidato")
    cover_letter = models.TextField(verbose_name="Carta de presentación", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied', verbose_name="Estado")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de aplicación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    notes = models.TextField(verbose_name="Notas del empleador", blank=True)

    class Meta:
        verbose_name = "Aplicación de trabajo"
        verbose_name_plural = "Aplicaciones de trabajo"
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.get_full_name() or self.applicant.username} - {self.job.title}"
