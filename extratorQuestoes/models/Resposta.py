
class Resposta:
    def __init__(self, id_prova, questao, enunciado, alternativa):
        self.id_prova = id_prova
        self.questao = questao
        self.alternativa = alternativa
        self.enunciado = enunciado

    def __str__(self):
        return f"{self.prova}; {self.questao}; {self.alternativa}; {self.enunciado}"
