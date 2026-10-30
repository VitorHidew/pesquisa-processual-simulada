import csv
from pathlib import Path

from src.modelos import Resultado


def exportar_csv(resultados: list[Resultado], caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["caso_id", "status", "movimentacoes", "observacao"])
        for item in resultados:
            escritor.writerow([item.caso_id, item.status, item.movimentacoes, item.observacao])
