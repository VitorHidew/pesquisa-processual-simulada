from dataclasses import dataclass


@dataclass(frozen=True)
class Caso:
    id: str
    parte_ficticia: str
    assunto_ficticio: str


@dataclass(frozen=True)
class Resultado:
    caso_id: str
    status: str
    movimentacoes: int
    observacao: str
