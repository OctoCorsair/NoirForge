"""Interface de linha de comando."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Sequence

from . import __version__, db
from .generator import MAX_SUSPECTS, MIN_SUSPECTS, generate_case
from .render import render_case

DEFAULT_DB = os.environ.get("NOIRFORGE_DB", "noirforge.db")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="noirforge",
        description="Gerador de casos de ficção policial (noir paulistano).",
    )
    parser.add_argument("--version", action="version", version=f"noirforge {__version__}")
    parser.add_argument("--db", default=DEFAULT_DB, help="caminho do banco SQLite")
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="gera um novo caso")
    new.add_argument("--seed", type=int, help="seed para reproduzir um caso")
    new.add_argument("--suspects", type=int, default=4,
                     help=f"número de suspeitos ({MIN_SUSPECTS} a {MAX_SUSPECTS})")
    new.add_argument("--save", action="store_true", help="salva no banco")
    new.add_argument("--solution", action="store_true", help="revela a solução")

    sub.add_parser("list", help="lista os casos salvos")

    show = sub.add_parser("show", help="mostra um caso salvo")
    show.add_argument("id", type=int)
    show.add_argument("--solution", action="store_true")

    export = sub.add_parser("export", help="exporta um caso para Markdown")
    export.add_argument("id", type=int)
    export.add_argument("--out", required=True, help="arquivo de saída (.md)")
    export.add_argument("--solution", action="store_true")

    delete = sub.add_parser("delete", help="apaga um caso salvo")
    delete.add_argument("id", type=int)

    sub.add_parser("stats", help="estatísticas dos casos salvos")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "new":
        try:
            case = generate_case(args.seed, args.suspects)
        except ValueError as exc:
            parser.error(str(exc))
        print(render_case(case, reveal=args.solution))
        if args.save:
            conn = db.connect(args.db)
            try:
                case_id = db.save_case(conn, case)
            finally:
                conn.close()
            print(f"💾 Caso salvo com id {case_id} em {args.db}")
        return 0

    conn = db.connect(args.db)
    try:
        if args.command == "list":
            rows = db.list_cases(conn)
            if not rows:
                print("Nenhum caso salvo ainda. Use: noirforge new --save")
            for r in rows:
                print(f"{r['id']:>3}  seed={r['seed']:<7} {r['num_suspects']} suspeitos  "
                      f"{r['era']:<16} {r['title']}")
            return 0

        if args.command in ("show", "export"):
            case = db.load_case(conn, args.id)
            if case is None:
                print(f"Caso {args.id} não encontrado.", file=sys.stderr)
                return 1
            text = render_case(case, reveal=args.solution)
            if args.command == "show":
                print(text)
            else:
                with open(args.out, "w", encoding="utf-8") as fh:
                    fh.write(text)
                print(f"📄 Exportado para {args.out}")
            return 0

        if args.command == "delete":
            if db.delete_case(conn, args.id):
                print(f"Caso {args.id} apagado.")
                return 0
            print(f"Caso {args.id} não encontrado.", file=sys.stderr)
            return 1

        if args.command == "stats":
            s = db.stats(conn)
            print(f"Casos salvos: {s['total']}")
            print("Armas mais comuns:")
            for name, n in s["weapons"]:
                print(f"  {n}x {name}")
            print("Relação mais comum do culpado com a vítima:")
            for name, n in s["culprit_relations"]:
                print(f"  {n}x {name}")
            return 0
    finally:
        conn.close()
    return 0
