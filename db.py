"""Persistência em SQLite."""

from __future__ import annotations

import sqlite3
from typing import Dict, List, Optional

from .generator import Case, Clue, Suspect

SCHEMA = """
CREATE TABLE IF NOT EXISTS cases (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    seed              INTEGER NOT NULL,
    num_suspects      INTEGER NOT NULL,
    title             TEXT NOT NULL,
    era               TEXT NOT NULL,
    place             TEXT NOT NULL,
    victim_name       TEXT NOT NULL,
    victim_occupation TEXT NOT NULL,
    weapon            TEXT NOT NULL,
    location          TEXT NOT NULL,
    twist             TEXT NOT NULL,
    created_at        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (seed, num_suspects)
);

CREATE TABLE IF NOT EXISTS suspects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id     INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    name        TEXT NOT NULL,
    relation    TEXT NOT NULL,
    motive      TEXT NOT NULL,
    alibi       TEXT NOT NULL,
    secret      TEXT NOT NULL,
    alibi_holds INTEGER NOT NULL,
    is_culprit  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS clues (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id     INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    position    INTEGER NOT NULL,
    kind        TEXT NOT NULL,
    text        TEXT NOT NULL,
    points_to   TEXT NOT NULL,
    explanation TEXT NOT NULL DEFAULT ''
);
"""


def connect(path: str = "noirforge.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def save_case(conn: sqlite3.Connection, case: Case) -> int:
    """Salva o caso e devolve o id. Salvar o mesmo caso duas vezes é idempotente."""
    n = len(case.suspects)
    existing = conn.execute(
        "SELECT id FROM cases WHERE seed = ? AND num_suspects = ?", (case.seed, n)
    ).fetchone()
    if existing:
        return existing["id"]

    with conn:
        cur = conn.execute(
            """INSERT INTO cases (seed, num_suspects, title, era, place, victim_name,
                                  victim_occupation, weapon, location, twist)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (case.seed, n, case.title, case.era, case.place, case.victim_name,
             case.victim_occupation, case.weapon, case.location, case.twist),
        )
        case_id = cur.lastrowid
        conn.executemany(
            """INSERT INTO suspects (case_id, position, name, relation, motive, alibi,
                                     secret, alibi_holds, is_culprit)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [(case_id, i, s.name, s.relation, s.motive, s.alibi, s.secret,
              int(s.alibi_holds), int(s.is_culprit))
             for i, s in enumerate(case.suspects)],
        )
        conn.executemany(
            """INSERT INTO clues (case_id, position, kind, text, points_to, explanation)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [(case_id, i, c.kind, c.text, c.points_to, c.explanation)
             for i, c in enumerate(case.clues)],
        )
    return case_id


def load_case(conn: sqlite3.Connection, case_id: int) -> Optional[Case]:
    row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    if row is None:
        return None
    suspects = [
        Suspect(r["name"], r["relation"], r["motive"], r["alibi"], r["secret"],
                bool(r["alibi_holds"]), bool(r["is_culprit"]))
        for r in conn.execute(
            "SELECT * FROM suspects WHERE case_id = ? ORDER BY position", (case_id,))
    ]
    clues = [
        Clue(r["kind"], r["text"], r["points_to"], r["explanation"])
        for r in conn.execute(
            "SELECT * FROM clues WHERE case_id = ? ORDER BY position", (case_id,))
    ]
    return Case(row["seed"], row["title"], row["era"], row["place"],
                row["victim_name"], row["victim_occupation"], row["weapon"],
                row["location"], row["twist"], suspects, clues)


def list_cases(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    return conn.execute(
        "SELECT id, seed, num_suspects, title, era, created_at FROM cases ORDER BY id"
    ).fetchall()


def delete_case(conn: sqlite3.Connection, case_id: int) -> bool:
    with conn:
        cur = conn.execute("DELETE FROM cases WHERE id = ?", (case_id,))
    return cur.rowcount > 0


def stats(conn: sqlite3.Connection) -> Dict[str, object]:
    total = conn.execute("SELECT COUNT(*) AS n FROM cases").fetchone()["n"]
    weapons = conn.execute(
        """SELECT weapon, COUNT(*) AS n FROM cases
           GROUP BY weapon ORDER BY n DESC, weapon LIMIT 3"""
    ).fetchall()
    relations = conn.execute(
        """SELECT relation, COUNT(*) AS n FROM suspects
           WHERE is_culprit = 1 GROUP BY relation ORDER BY n DESC, relation LIMIT 3"""
    ).fetchall()
    return {
        "total": total,
        "weapons": [(r["weapon"], r["n"]) for r in weapons],
        "culprit_relations": [(r["relation"], r["n"]) for r in relations],
    }
