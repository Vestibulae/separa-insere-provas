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
            print(err)
            trans.rollback()


def insertGabarito(prova_id, questao_id, alternativa):
    with db.atomic() as trans:
        try:
            Gabaritos.create(prova_id=prova_id,
                             questao_id=questao_id, alternativa=alternativa)
            trans.commit()
        except DatabaseError as err:
            print(err)
            trans.rollback()


def insertQuestao(questao):
    with db.atomic() as trans:
        try:
            questao.save()
            trans.commit()
            return questao
        except DatabaseError as err:
            print(err)
            trans.rollback()
            return getQuestao(prova=questao.prova_id, numero=questao.numero, materia=questao.materia)


def getQuestao(prova, numero, materia):
    with db.atomic() as trans:
        try:
            questao = Questoes.get(Questoes.prova_id == prova, Questoes.numero ==
                                   numero, Questoes.materia == materia)
            trans.commit()
            return questao
        except Questoes.DoesNotExist as err:
            print(err, f"data: {prova}, {numero}, {materia}")


def getIdProva(nome_prova, dados_prova):
    with db.atomic() as trans:
        try:
            id_prova = Provas.get(Provas.prova == nome_prova, Provas.ano ==
                                  dados_prova[0], Provas.fase == dados_prova[1]).id
            trans.commit()
            return id_prova
        except Provas.DoesNotExist as err:
            print(err, f"data: {nome_prova}, {dados_prova}")
