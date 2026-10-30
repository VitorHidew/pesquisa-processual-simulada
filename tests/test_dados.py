from pathlib import Path

import pytest

from src.dados import carregar_casos


def test_carrega_apenas_identificadores_simulados():
    casos = carregar_casos(Path("data/casos_ficticios.jsonl"))
    assert len(casos) == 12
    assert all(caso.id.startswith("SIM-") for caso in casos)


def test_rejeita_identificador_realista(tmp_path):
    arquivo = tmp_path / "casos.jsonl"
    arquivo.write_text(
        '{"id":"CASO-INVALIDO","parte_ficticia":"Exemplo","assunto_ficticio":"Exemplo"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="SIM-"):
        carregar_casos(arquivo)
