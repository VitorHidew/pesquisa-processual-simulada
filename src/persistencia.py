import sqlite3
from pathlib import Path

from src.modelos import Resultado


class Progresso:
    def __init__(self, caminho: Path):
        caminho.parent.mkdir(parents=True, exist_ok=True)
        self.conexao = sqlite3.connect(caminho, check_same_thread=False)
        self.conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS resultados (
                caso_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                movimentacoes INTEGER NOT NULL,
                observacao TEXT NOT NULL
            )
            """
        )
        self.conexao.commit()

    def concluidos(self) -> set[str]:
        linhas = self.conexao.execute("SELECT caso_id FROM resultados").fetchall()
        return {linha[0] for linha in linhas}

    def salvar(self, resultado: Resultado) -> None:
        self.conexao.execute(
            """
            INSERT INTO resultados (caso_id, status, movimentacoes, observacao)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(caso_id) DO UPDATE SET
                status=excluded.status,
                movimentacoes=excluded.movimentacoes,
                observacao=excluded.observacao
            """,
            (resultado.caso_id, resultado.status, resultado.movimentacoes, resultado.observacao),
        )
        self.conexao.commit()

    def listar(self) -> list[Resultado]:
        linhas = self.conexao.execute(
            "SELECT caso_id, status, movimentacoes, observacao FROM resultados ORDER BY caso_id"
        ).fetchall()
        return [Resultado(*linha) for linha in linhas]

    def fechar(self) -> None:
        self.conexao.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.fechar()
