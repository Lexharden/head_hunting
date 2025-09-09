from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'location', 'size', 'industry', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CompanyListView(ListView):
    model = Company
    template_name = 'companies/list.html'
    context_object_name = 'companies'
    paginate_by = 12

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = self.object.job_set.filter(is_active=True)
        return context

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/create.html'
    success_url = reverse_lazy('companies:my_company')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/edit.html'
    success_url = reverse_lazy('companies:my_company')

    def get_queryset(self):
        return Company.objects.filter(created_by=self.request.user)

class MyCompanyView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/my_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.filter(created_by=self.request.user)
        return context
