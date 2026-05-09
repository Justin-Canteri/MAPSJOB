from django.urls import path
from .views import views
from .views import ofertas

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns =[
    path('', views.inicio),
    path('crear_oferta/', ofertas.post),
    path('buscarID/', ofertas.getMisOfertas)
]