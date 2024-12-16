from django.db import models

class Jogador(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    pontuacao_total = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Fase(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    desbloqueada = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Pontuacao(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    pontuacao = models.IntegerField()

    def __str__(self):
        return f'{self.jogador} - {self.fase} - {self.pontuacao}'
