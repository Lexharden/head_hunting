from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django import forms
from .models import Job, JobApplication
from companies.models import Company

class JobSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Buscar", 
                       widget=forms.TextInput(attrs={'placeholder': 'Título del puesto, empresa, habilidades...'}))
    location = forms.CharField(required=False, label="Ubicación",
                              widget=forms.TextInput(attrs={'placeholder': 'Ciudad, país...'}))
    job_type = forms.ChoiceField(required=False, choices=[('', 'Todos')] + Job.JOB_TYPES, label="Tipo de trabajo")
    experience_level = forms.ChoiceField(required=False, choices=[('', 'Todos')] + Job.EXPERIENCE_LEVELS, label="Nivel de experiencia")
    remote_work = forms.BooleanField(required=False, label="Trabajo remoto")

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description', 'requirements', 'location', 'job_type', 
                 'experience_level', 'salary_min', 'salary_max', 'currency', 'remote_work', 
                 'skills_required', 'expires_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'skills_required': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Separar habilidades con comas'}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Company.objects.filter(created_by=user)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Explica por qué eres el candidato ideal para este puesto...'})
        }

class JobListView(ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        form = JobSearchForm(self.request.GET)
        
        if form.is_valid():
            q = form.cleaned_data.get('q')
            location = form.cleaned_data.get('location')
            job_type = form.cleaned_data.get('job_type')
            experience_level = form.cleaned_data.get('experience_level')
            remote_work = form.cleaned_data.get('remote_work')

            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) | 
                    Q(company__name__icontains=q) | 
                    Q(description__icontains=q) |
                    Q(skills_required__icontains=q)
                )
            if location:
                queryset = queryset.filter(location__icontains=location)
            if job_type:
                queryset = queryset.filter(job_type=job_type)
            if experience_level:
                queryset = queryset.filter(experience_level=experience_level)
            if remote_work:
                queryset = queryset.filter(remote_work=True)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET)
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = JobApplication.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()
        return context

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/create.html'
    success_url = reverse_lazy('jobs:my_jobs')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/edit.html'
    success_url = reverse_lazy('jobs:my_jobs')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class JobApplicationView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/apply.html'

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=kwargs['pk'])
        if JobApplication.objects.filter(job=self.job, applicant=request.user).exists():
            messages.warning(request, 'Ya has aplicado a esta oferta de trabajo.')
            return redirect('jobs:detail', pk=self.job.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.job = self.job
        form.instance.applicant = self.request.user
        messages.success(self.request, 'Tu aplicación ha sido enviada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('jobs:detail', kwargs={'pk': self.job.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context

class MyJobsView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/my_jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.filter(posted_by=self.request.user).order_by('-created_at')
        return context

class MyApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/my_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = JobApplication.objects.filter(
            applicant=self.request.user
        ).order_by('-applied_at')
        return context
