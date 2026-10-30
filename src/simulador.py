import hashlib
import time

from src.modelos import Caso, Resultado


STATUS = ("em_andamento", "concluido", "aguardando_revisao")


def pesquisar(caso: Caso, pausa: float = 0.0) -> Resultado:
    if pausa < 0:
        raise ValueError("A pausa não pode ser negativa.")
    if pausa:
        time.sleep(pausa)

    digest = hashlib.sha256(f"{caso.id}|{caso.assunto_ficticio}".encode()).digest()
    status = STATUS[digest[0] % len(STATUS)]
    movimentacoes = 1 + digest[1] % 8
    return Resultado(
        caso_id=caso.id,
        status=status,
        movimentacoes=movimentacoes,
        observacao="Resultado gerado localmente em modo simulado.",
    )
