"""Renderização de casos em Markdown."""

from __future__ import annotations

from .generator import TRUE_CLUE, Case


def render_case(case: Case, reveal: bool = False) -> str:
    lines = [
        f"# {case.title}",
        f"*{case.era} · seed {case.seed}*",
        "",
        f"**Vítima:** {case.victim_name}, {case.victim_occupation}.",
        f"**Cena do crime:** o corpo foi encontrado {case.location}, {case.place}.",
        f"**Arma:** {case.weapon}.",
        "",
        "## Suspeitos",
    ]
    for s in case.suspects:
        lines.append(
            f"- **{s.name}** ({s.relation}): motivo, {s.motive}; {s.alibi}."
        )

    lines += ["", "## Evidências"]
    for i, clue in enumerate(case.clues, 1):
        lines.append(f"{i}. {clue.text}")
        if reveal:
            if clue.kind == TRUE_CLUE:
                lines.append(f"   - ✅ Pista verdadeira, aponta para {clue.points_to}.")
            else:
                lines.append(f"   - ❌ Falsa pista: {clue.explanation}")

    if reveal:
        culprit = case.culprit
        lines += [
            "",
            "## Solução",
            f"**Culpado:** {culprit.name} ({culprit.relation}).",
            f"**Motivo:** {culprit.motive}.",
            f"**Álibi furado:** {culprit.name} {culprit.alibi}, mas a história não se sustenta.",
            f"**Reviravolta:** {case.twist}",
        ]
    else:
        lines += ["", "> 🔎 Quem fez isso? Revele com `--solution` quando estiver pronto."]
    return "\n".join(lines) + "\n"
