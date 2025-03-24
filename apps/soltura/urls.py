from django.urls import path
from .views import listar_colaboradores, criar_soltura
urlpatterns = [
    path('colaboradores/', listar_colaboradores, name='listar_colaboradores'),
    path('solturas/criar/', criar_soltura, name='criar_soltura'),
]

