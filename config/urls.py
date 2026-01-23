from django.contrib import admin
from django.urls import path, include # <--- Importe o include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('runner/', include('runner_sheet.urls')), # <--- Adicione isso
]