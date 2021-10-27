from util.db import db
from peewee import DatabaseError
from util.models import Provas, Questoes, Respostas, Gabaritos


def insertProva(prova):
    with db.atomic() as trans:
        try:
            prova.save()
            trans.commit()
        except DatabaseError as err:
            print(err, f"data: {prova}")
            trans.rollback()


def insertRespostas(respostas):
    with db.atomic() as trans:
        try:
            Respostas.bulk_create(respostas)
            trans.commit()
        except DatabaseError as err:
            print(err, f"data: {respostas}")
            trans.rollback()


def insertQuestoes(questoes):
    with db.atomic() as trans:
        try:
            Questoes.bulk_create(questoes)
            trans.commit()
        except DatabaseError as err:
            print(err, f"data: {questoes}")
            trans.rollback()


def getProva(nome_prova, dados_prova):
    try:
        db.connect()
        prova = Provas.get(Provas.prova == nome_prova, Provas.ano ==
                           dados_prova[0], Provas.fase == dados_prova[1]).id
        db.close()
        return prova
    except Provas.DoesNotExist as err:
        print(err, f"data: {nome_prova}, {dados_prova}")
