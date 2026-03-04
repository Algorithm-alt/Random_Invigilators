from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    
    path('centers/', views.center_list, name='center_list'),
    path('centers/add/', views.center_create, name='center_create'),
    path('centers/<int:pk>/edit/', views.center_update, name='center_update'),
    path('centers/<int:pk>/delete/', views.center_delete, name='center_delete'),
    
    path('generate-assignments/', views.generate_assignments, name='generate_assignments'),
    path('export-assignments/', views.export_assignments, name='export_assignments'),
]
