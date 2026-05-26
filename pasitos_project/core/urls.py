from django.urls import path
from . import views

urlpatterns = [
    # Pantalla de inicio / carga
    path('', views.pantalla_carga, name='pantalla_carga'),
    
    # Registro y selección de perfil para el niño
    path('crear-perfil/', views.crear_perfil, name='crear_perfil'),
    
    # Dashboards infantiles según el rango de edad
    path('contenido-3-4/', views.dashboard_baja, name='dashboard_infantil_baja'),
    path('contenido-5-7/', views.dashboard_alta, name='dashboard_infantil_alta'),
    
    # Visualización del perfil del alumno activo
    path('perfil-alumno/', views.perfil_alumno_view, name='perfil_alumno'),
    
    # Nueva ruta: Filtro de seguridad y panel de control de los padres
    path('panel-tutores/', views.panel_tutores, name='panel_tutores'),
    
    
    
]