from django.contrib import admin
from django.urls import path
from app.views import *  # Importação das classes de views

urlpatterns = [
    path('admin/', admin.site.urls),  # URL do painel de administração
    path('', IndexView.as_view(), name='index'),  # Página inicial
    path('fases/', FasesView.as_view(), name='fases'),  # Página de fases
    path('fases/<int:fase_id>/', IniciarFaseView.as_view(), name='iniciar_fase'),  # Página de uma fase específica
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),  # Página do ranking
]
