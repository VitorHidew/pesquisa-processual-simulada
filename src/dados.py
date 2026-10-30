import json
from pathlib import Path

from src.modelos import Caso


def carregar_casos(caminho: Path) -> list[Caso]:
    casos: list[Caso] = []
    with caminho.open(encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            if not linha.strip():
                continue
            try:
                item = json.loads(linha)
                caso = Caso(
                    id=str(item["id"]),
                    parte_ficticia=str(item["parte_ficticia"]),
                    assunto_ficticio=str(item["assunto_ficticio"]),
                )
            except (KeyError, TypeError, json.JSONDecodeError) as erro:
                raise ValueError(f"Linha {numero_linha} inválida em {caminho.name}.") from erro
            if not caso.id.startswith("SIM-"):
                raise ValueError(f"Linha {numero_linha}: identificador deve começar com SIM-.")
            casos.append(caso)
    return casos
