"""
ARQUIVO: urls.py
OBJETIVO: Define as rotas principais (URLs) do site.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Painel Administrativo (para criar personagens/armas)
    path('admin/', admin.site.urls),
    
    # [ROTA PRINCIPAL]
    # Deixamos vazio ('') para que o site abra direto na Home.
    # Inclui todas as URLs definidas dentro de runner_sheet/urls.py
    path('', include('runner_sheet.urls')),
]

# [CONFIGURAÇÃO DE DESENVOLVIMENTO]
# Este bloco permite que o Django sirva as imagens de upload (Media)
# enquanto estamos com DEBUG = True.
# Sem isso, as fotos dos personagens apareceriam quebradas no localhost.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)