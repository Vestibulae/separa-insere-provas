
from peewee import *
from ..util.db import db
import Prova


class Questao(Model):

    id_prova = ForeignKeyField(Prova)
    numero = SmallIntegerField()
    materia = CharField()
    enunciado = TextField()
    imagem = CharField()

    class Meta:
        database = db
        primary_key = CompositeKey('id_prova', 'numero')

    # def __str__(self):
    #     return f"{self.id_prova}; {self.numero}; {self.materia}; {self.enunciado}; {self.imagem}"
