from django.urls import path
from LoginFaceDetection import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu_sesion', views.menuLogueo, name='session_menu'),
    path('iniciar_sesion', views.loguear, name='sesion'),
    path('sesion_facial', views.loguear_facial, name='sesion_facial'),
    path('menu_registro', views.reg_menu, name='reg_menu'),
    path('registrarse', views.registrarse, name='register'),
    path('registro_facial', views.register_facial, name='reg_facial'),
    path('procesar/', views.procesar_sesion),
    path('proceso_register/', views.proceso_register),
    path('cap_face/', views.cap_face),
    path('facial_log/', views.facial_log),
]