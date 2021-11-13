# TAGS NAS PROVAS:
# @ = Questao
# \L = Link (imagem)
# \ = inicio e fim das respostas
# # = nova alternativa
# @@ = materia
from util.models import *
from util.controller import insertProva, insertQuestao, insertRespostas, getIdProva, insertGabarito
from util.db import db


def separaProva(linha):

    lista_prova = linha[1:].split(";")
    nome_prova = lista_prova[0]
    prova = Provas(
        prova=lista_prova[0], ano=lista_prova[1], fase=lista_prova[2], descricao=lista_prova[3])
    insertProva(prova)
    return nome_prova


def separaDados(prova, gabarito):

    prova_aberta = open(prova, encoding="utf8")
    gabarito_aberto = open(gabarito, encoding="utf8")

    nome_prova = None
    id_prova = None
    dados_prova = None
    materia = None
    numero = None
    enunciado = ""
    imagem = None

    for linha in prova_aberta:

        if linha[0] == "|":
            nome_prova = separaProva(linha)
            continue

        elif linha[0] == "@":

            if linha[1] != "@":
                numero = linha[1:4].strip()
                aux = linha[5:].strip("\n ()").split(".")
                if dados_prova != aux:
                    dados_prova = aux
                    id_prova = getIdProva(nome_prova, dados_prova)
                continue
            else:
                materia = linha[2:].strip("\n ")
                continue

        elif linha[0] == "\\":

            if linha[1] == "L":
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{materia}_{numero}"
                enunciado += linha
                continue

            else:
                enunciado = enunciado.strip("\n")
                questao = Questoes(prova_id=id_prova, numero=numero,
                                   materia=materia, enunciado=enunciado, imagem=imagem)
                questao_salva = insertQuestao(questao)
                separaRespostas(
                    nome_prova=nome_prova, dados_prova=dados_prova, questao=questao_salva, prova=prova_aberta, gabarito=gabarito_aberto.readline())
                enunciado = ""
                imagem = None
                continue

        else:
            enunciado += linha

    prova_aberta.close()
    gabarito_aberto.close()
    return 0


def separaRespostas(nome_prova, dados_prova, questao, prova, gabarito):
    alternativa = None
    enunciado = "None"
    imagem = None
    lista_respostas = []
    for linha in prova:
        if linha[0] == "\\":
            if "\L" in enunciado:
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{questao.materia}_{questao.numero}_{alternativa}"

            resposta = Respostas(prova_id=questao.prova_id, questao_id=questao.id,
                                 enunciado=enunciado, alternativa=alternativa, imagem=imagem)
            lista_respostas.append(resposta)
            break

        elif linha[0] in ['A', 'B', 'C', 'D', 'E'] and linha[1] == ")":
            if "\L" in enunciado:
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{questao.materia}_{questao.numero}_{alternativa}"

            if alternativa != None and enunciado != None:
                resposta = Respostas(prova_id=questao.prova_id, questao_id=questao.id,
                                     enunciado=enunciado, alternativa=alternativa, imagem=imagem)
                lista_respostas.append(resposta)
                imagem = None

            alternativa = linha[0].upper()
            enunciado = linha[3:].strip("\n")

        else:
            enunciado += linha.strip("\n")

    if lista_respostas:
        insertRespostas(lista_respostas)
        gabarito = gabarito.strip(" \n").split()
        insertGabarito(prova_id=questao.prova_id,
                       questao_id=questao.id, alternativa=gabarito[1])
    else:
        print(
            f"ERROR - Lista de Respostas Vazia! Respostas da questão {questao} não inseridas!")
    return 0


db.connect()
db.create_tables([Provas, Questoes, Respostas, Gabaritos])
db.close()


# print(insertGabarito("Provas/2020_GB_impresso_D1_CD4.txt"))
separaDados("Provas/txt/matematica.txt",
            "Provas/txt/gabaritos/gabarito_matematica.txt")
# teste("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
