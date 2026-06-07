import json
import os

ARQUIVO = "ranking.json"

def carregar():

    if not os.path.exists(ARQUIVO):
        return []

    with open(
        ARQUIVO,
        "r",
        encoding="utf8"
    ) as arquivo:

        return json.load(arquivo)

def salvar_pontuacao(
    pontos,
    turnos
):

    ranking = carregar()

    ranking.append({

        "pontos": pontos,
        "turnos": turnos

    })

    ranking.sort(
        key=lambda x: x["pontos"],
        reverse=True
    )

    ranking = ranking[:10]

    with open(
        ARQUIVO,
        "w",
        encoding="utf8"
    ) as arquivo:

        json.dump(
            ranking,
            arquivo,
            indent=4,
            ensure_ascii=False
        )

    return ranking