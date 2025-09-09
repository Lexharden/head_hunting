from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='detail'),
    path('create/', views.JobCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='edit'),
    path('<int:pk>/apply/', views.JobApplicationView.as_view(), name='apply'),
    path('my-jobs/', views.MyJobsView.as_view(), name='my_jobs'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
]