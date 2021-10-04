# TAGS NAS PROVAS:
# @ = Questao
# \L = Link (imagem)
# \ = inicio das respostas
# \E = Fim das respostas
#  @@ = materia
from models.Gabarito import Gabarito
from models.Resposta import Resposta
from models.Questao import Questao
from models.Prova import Prova


def insertProvas():
    pass


def separaQuestoes(arquivo):
    file = open(arquivo, encoding="utf8")
    prova = file.readline().strip("\n").split(" ")
    id_prova = None  # fazer consulta no banco procurar pelas chaves da lista prova
    materia = None
    numero = None
    enunciado = ""
    imagem = None
    lista = []
    for linha in file:

        if linha[0] == "@":

            if linha[1] != "@":
                numero = linha[1:].strip("\n").strip(" ")
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
                questao = Questao(id_prova, numero, materia, enunciado, imagem)
                lista.append(questao)
                separaRespostas(prova, id_prova, numero, file)
                enunciado = ""
                imagem = None
                continue

        else:
            enunciado += linha
    # lista.save()
    return 0


def separaRespostas(prova, id_prova, numero, file):
    alternativa = None
    enunciado = "None"
    lista = []
    for linha in file:
        if linha[0] == "\\":
            alternativa = linha[1].upper()
            enunciado = linha[2:].strip("\n")
            if "\L" in enunciado:
                enunciado = f"{prova[0]}/{prova[1]}/{prova[2]}/{numero}_{alternativa}"
            resposta = Resposta(id_prova, numero, enunciado, alternativa)
            lista.append(resposta)
            break

        else:
            alternativa = linha[0].upper()
            enunciado = linha[1:].strip("\n")
            if "\L" in enunciado:
                enunciado = f"{prova[0]}/{prova[1]}/{prova[2]}/{numero}_{alternativa}"
            resposta = Resposta(id_prova, numero, enunciado, alternativa)
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
separaQuestoes("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
# teste("Provas/2020_PV_impresso_D1_CD4_superampliada.txt")
