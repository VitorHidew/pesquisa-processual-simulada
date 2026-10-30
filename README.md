# Pesquisa Processual Simulada em Python

Pipeline local para demonstrar processamento em lotes, paralelismo, retomada e exportação de resultados usando somente casos fictícios.

> Este projeto não acessa tribunais, portais públicos, navegadores ou APIs externas. Os identificadores `SIM-*`, nomes, assuntos e resultados são inventados.

## Objetivo

O projeto transforma um fluxo de pesquisa repetitiva em uma demonstração segura para portfólio. A execução simula consultas de forma determinística, registra cada resultado em SQLite e permite retomar um lote sem repetir o que já foi concluído.

## Funcionalidades

- leitura de casos JSON Lines;
- validação obrigatória do prefixo fictício `SIM-`;
- modo `--simulado` obrigatório;
- processamento paralelo com limite configurável;
- pausa opcional entre tarefas;
- seleção por início e quantidade;
- persistência incremental em SQLite;
- retomada automática;
- exportação CSV.

## Requisitos

- Python 3.12+
- Pytest apenas para desenvolvimento

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Execução

```powershell
python -m src.cli --simulado --inicio 0 --quantidade 5 --trabalhadores 2 --pausa 0
```

Arquivos locais gerados:

- `results/progresso.sqlite`: progresso e cache;
- `results/resultado.csv`: exportação consolidada.

Ambos são ignorados pelo Git. Uma nova execução com o mesmo banco pula automaticamente os casos já salvos.

## Executar em partes

```powershell
python -m src.cli --simulado --inicio 0 --quantidade 4
python -m src.cli --simulado --inicio 4 --quantidade 4
python -m src.cli --simulado --inicio 8 --quantidade 4
```

## Testes

```powershell
python -m pytest -q -p no:cacheprovider
```

## Estrutura

```text
src/      pipeline, simulador, persistência e exportação
data/     casos exclusivamente fictícios
tests/    testes automatizados
results/  saída local ignorada pelo Git
```

## Limitações e uso responsável

- não existe integração com sistemas judiciais reais;
- o resultado é derivado de hash e não representa andamento processual;
- os dados não devem ser usados para decisões jurídicas;
- qualquer integração futura exigiria autorização, revisão dos termos do portal, proteção de dados e supervisão humana;
- a ferramenta não substitui profissionais ou fontes oficiais.

## Resultados

| Indicador | Resultado |
|---|---|
| Tempo de processamento | [PREENCHER] |
| Casos processados | [PREENCHER] |
| Casos retomados do cache | [PREENCHER] |

## Licença

MIT. Consulte `LICENSE`.
