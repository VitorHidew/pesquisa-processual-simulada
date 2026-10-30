import argparse
import csv
from pathlib import Path

from src.cli import executar
from src.dados import carregar_casos
from src.simulador import pesquisar


def argumentos(tmp_path: Path) -> argparse.Namespace:
    return argparse.Namespace(
        simulado=True,
        casos=Path("data/casos_ficticios.jsonl"),
        banco=tmp_path / "progresso.sqlite",
        saida=tmp_path / "resultado.csv",
        inicio=0,
        quantidade=4,
        trabalhadores=2,
        pausa=0.0,
    )


def test_simulador_e_deterministico():
    caso = carregar_casos(Path("data/casos_ficticios.jsonl"))[0]
    assert pesquisar(caso) == pesquisar(caso)


def test_lote_exporta_csv_e_retomada_pula_concluidos(tmp_path):
    args = argumentos(tmp_path)
    primeira = executar(args)
    segunda = executar(args)

    assert primeira == {"processados": 4, "ignorados": 0, "selecionados": 4}
    assert segunda == {"processados": 0, "ignorados": 4, "selecionados": 4}
    with args.saida.open(encoding="utf-8-sig") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert len(linhas) == 4


def test_modo_simulado_e_obrigatorio(tmp_path):
    args = argumentos(tmp_path)
    args.simulado = False
    try:
        executar(args)
    except ValueError as erro:
        assert "--simulado" in str(erro)
    else:
        raise AssertionError("Execução sem --simulado deveria falhar.")
