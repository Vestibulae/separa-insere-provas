# TAGS NAS PROVAS:
# @ = Questao
# \L = Link (imagem)
# \ = inicio e fim das respostas
# # = nova alternativa
# @@ = materia
from util.models import Provas, Questoes, Respostas, Gabaritos
from util.controller import insertProva, insertQuestoes, insertRespostas, getProva


def separaDados(arquivo):
    file = open(arquivo, encoding="utf8")
    # prova = file.readline().strip("\n").split(" ")
    nome_prova = None
    id_prova = None  # fazer consulta no banco procurar pelas chaves da lista prova
    dados_prova = None
    materia = None
    numero = None
    enunciado = ""
    imagem = None
    lista = []
    for linha in file:

        if linha[0] == "|":
            lista_prova = linha[1:].split(";")
            nome_prova = lista_prova[0]
            prova = Provas(
                prova=lista_prova[0], ano=lista_prova[1], fase=lista_prova[2], descricao=lista_prova[3])
            insertProva(prova)
            continue

        elif linha[0] == "@":

            if linha[1] != "@":
                numero = linha[1:4].strip(" ")
                aux = linha[4:].strip("\n").strip(
                    " ").strip("(").strip(")").split(".")
                if not dados_prova == aux:
                    dados_prova = aux
                    id_prova = getProva(nome_prova, dados_prova)
                continue
            else:
                materia = linha[2:].strip("\n")
                continue

        elif linha[0] == "\\":

            if linha[1] == "L":
                imagem = f"{prova[0]}/{prova[1]}/{prova[2]}/{numero}"
                continue
            elif linha[1] == "E":
                enunciado = ""
                continue
            else:
                questao = Questoes(
                    id_prova, numero, materia, enunciado, imagem)
                lista.append(questao)
                separaRespostas(prova, id_prova, numero, file)
                enunciado = ""
                imagem = None
                continue

        else:
            enunciado += linha
    insertQuestoes(lista)
    return 0


def separaRespostas(prova, id_prova, numero, file):
    alternativa = None
    enunciado = "None"
    lista = []
    for linha in file:
        if linha[0] == "\\":
            with
            Respostas.bulk_create(lista)
            break

        elif linha[0] == "#":
            alternativa = linha[1].upper()
            enunciado = linha[3:].strip("\n")
            if "\L" in enunciado:
                enunciado = f"{prova[0]}/{prova[1]}/{prova[2]}/{numero}_{alternativa}"
            resposta = Respostas(id_prova, numero, enunciado, alternativa)
            lista.append(resposta)

        else:
            alternativa = linha[0].upper()
            enunciado = linha[1:].strip("\n")
            if "\L" in enunciado:
                enunciado = f"{prova[0]}/{prova[1]}/{prova[2]}/{numero}_{alternativa}"
            resposta = Respostas(id_prova, numero, enunciado, alternativa)
            lista.append(resposta)
            continue

    # lista.save()
    return 0


def insertGabarito(arquivo):
    file = open(arquivo, encoding="utf8")

    lista = []
    for linha in file:
        a = linha
        if a[-1] == "\n":
            a = a[:-1]

        a = a.split(" ")
        lista.append(a)

    # lista.save()
    return 0


# print(insertGabarito("Provas/2020_GB_impresso_D1_CD4.txt"))
separaDados("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
# teste("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
