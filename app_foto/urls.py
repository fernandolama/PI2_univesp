from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/edit/<int:pk>/', views.client_edit, name='client_edit'),
    path('clients/delete/<int:pk>/', views.client_delete, name='client_delete'),

    path('services/', views.service_list, name='service_list'),
    path('services/new/', views.service_create, name='service_create'),
    path('services/edit/<int:pk>/', views.service_edit, name='servicoe_edit'),
    path('services/delete/<int:pk>/', views.service_delete, name='service_delete'),

]  #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)