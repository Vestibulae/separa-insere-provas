# TAGS NAS PROVAS:
# @ = Questao
# \L = Link (imagem)
# \ = inicio e fim das respostas
# # = nova alternativa
# @@ = materia
from util.models import Provas, Questoes, Respostas, Gabaritos
from util.controller import insertProva, insertQuestao, insertRespostas, getIdProva


def separaProva(linha):

    lista_prova = linha[1:].split(";")
    nome_prova = lista_prova[0]
    prova = Provas(
        prova=lista_prova[0], ano=lista_prova[1], fase=lista_prova[2], descricao=lista_prova[3])
    insertProva(prova)
    return nome_prova


def separaDados(arquivo):

    file = open(arquivo, encoding="utf8")
    nome_prova = None
    id_prova = None  # fazer consulta no banco procurar pelas chaves da lista prova
    dados_prova = None
    materia = None
    numero = None
    enunciado = ""
    imagem = None

    for linha in file:

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
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{numero}"
                enunciado += linha
                continue

            else:
                questao = Questoes(prova_id=id_prova, numero=numero,
                                   materia=materia, enunciado=enunciado, imagem=imagem)
                questao_salva = insertQuestao(questao)
                separaRespostas(
                    nome_prova=nome_prova, dados_prova=dados_prova, questao=questao_salva, file=file)
                enunciado = ""
                imagem = None
                continue

        else:
            enunciado += linha

    return 0


def separaRespostas(nome_prova, dados_prova, questao, file):
    alternativa = None
    enunciado = "None"
    imagem = None
    lista_respostas = []
    for linha in file:
        if linha[0] == "\\":
            if "\L" in enunciado:
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{questao.numero}_{alternativa}"

            resposta = Respostas(prova_id=questao.prova_id, questao_id=questao.id,
                                 enunciado=enunciado, alternativa=alternativa, imagem=imagem)
            lista_respostas.append(resposta)
            break

        elif linha[0] in ['A', 'B', 'C', 'D', 'E'] and linha[1] == ")":
            if "\L" in enunciado:
                imagem = f"{nome_prova}/{dados_prova[0]}/{dados_prova[1]}/{questao.numero}_{alternativa}"

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
    else:
        print(
            f"ERROR - Lista de Respostas Vazia! Respostas da questão {questao} não inseridas!")
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
separaDados("Provas/portugues.txt")
# teste("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
