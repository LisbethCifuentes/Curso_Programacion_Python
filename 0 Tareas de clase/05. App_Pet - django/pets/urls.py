from django.urls import path
from .views import (
    pets_page,
    pets_api_list,
    pets_api_detail,
)

urlpatterns = [
    # Vista renderizada (HTML) - SIN autenticación
    path('', pets_page, name='pets_page'),
    
    # API endpoints - CON JWT
    path('api/pets/', pets_api_list, name='api_pets_list'),
    path('api/pets/<str:pet_id>/', pets_api_detail, name='api_pets_detail'),
]