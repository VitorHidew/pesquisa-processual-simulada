import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.dados import carregar_casos
from src.exportacao import exportar_csv
from src.persistencia import Progresso
from src.simulador import pesquisar


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pesquisa local com dados processuais fictícios.")
    parser.add_argument("--simulado", action="store_true", help="Confirma o uso do simulador local.")
    parser.add_argument("--casos", type=Path, default=Path("data/casos_ficticios.jsonl"))
    parser.add_argument("--banco", type=Path, default=Path("results/progresso.sqlite"))
    parser.add_argument("--saida", type=Path, default=Path("results/resultado.csv"))
    parser.add_argument("--inicio", type=int, default=0)
    parser.add_argument("--quantidade", type=int, default=5)
    parser.add_argument("--trabalhadores", type=int, default=2)
    parser.add_argument("--pausa", type=float, default=0.0)
    return parser


def executar(args: argparse.Namespace) -> dict[str, int]:
    if not args.simulado:
        raise ValueError("Use --simulado. Este projeto não acessa portais reais.")
    if args.inicio < 0 or args.quantidade < 1 or args.trabalhadores < 1:
        raise ValueError("Início, quantidade e trabalhadores devem ser válidos.")

    lote = carregar_casos(args.casos)[args.inicio : args.inicio + args.quantidade]
    processados = 0
    ignorados = 0
    with Progresso(args.banco) as progresso:
        concluidos = progresso.concluidos()
        pendentes = []
        for caso in lote:
            if caso.id in concluidos:
                ignorados += 1
            else:
                pendentes.append(caso)

        with ThreadPoolExecutor(max_workers=args.trabalhadores) as executor:
            futuros = {executor.submit(pesquisar, caso, args.pausa): caso for caso in pendentes}
            for futuro in as_completed(futuros):
                progresso.salvar(futuro.result())
                processados += 1

        exportar_csv(progresso.listar(), args.saida)
    return {"processados": processados, "ignorados": ignorados, "selecionados": len(lote)}


def main() -> int:
    parser = criar_parser()
    args = parser.parse_args()
    try:
        resumo = executar(args)
    except ValueError as erro:
        parser.error(str(erro))
    print(
        f"Simulação concluída: {resumo['processados']} processados, "
        f"{resumo['ignorados']} retomados do cache, {resumo['selecionados']} selecionados."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
