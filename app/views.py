import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View  # Importação necessária para as views baseadas em classes
from .models import Jogador, Fase, Pontuacao

class IndexView(View):
    """ Exibe a página inicial """
    def get(self, request):
        return render(request, 'index.html')


class FasesView(View):
    """ Exibe a lista de fases disponíveis """
    def get(self, request):
        fases = Fase.objects.all()
        return render(request, 'fases.html', {'fases': fases})


class IniciarFaseView(View):
    """ Inicia uma fase específica do jogo """
    def get(self, request, fase_id):
        """
        Inicia o jogo SkyJump e passa o ID da fase para o script skyjump.py.
        """
        # Obtém a fase ou retorna um erro 404 se a fase não existir
        fase = get_object_or_404(Fase, id=fase_id)
        
        # Caminho absoluto para o arquivo skyjump.py
        caminho_skyjump = os.path.join(os.path.dirname(__file__), 'static', 'game', 'skyjump.py')
        
        try:
            # Executa o script skyjump.py e passa o ID da fase como argumento
            subprocess.Popen(['python', caminho_skyjump, str(fase_id)])
        except Exception as e:
            print(f"Erro ao iniciar o jogo: {e}")
        
        # Redireciona para a página inicial ou qualquer outra que você prefira
        return redirect('index')


class LeaderboardView(View):
    """ Exibe o ranking de pontuações """
    def get(self, request):
        ranking = Pontuacao.objects.all().order_by('-pontuacao')[:10]
        return render(request, 'leaderboard.html', {'ranking': ranking})
