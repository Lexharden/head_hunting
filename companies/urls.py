from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='list'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='detail'),
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='edit'),
    path('my-company/', views.MyCompanyView.as_view(), name='my_company'),
]