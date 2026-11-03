"""Gerador determinístico de casos policiais."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

from . import data

MIN_SUSPECTS = 3
MAX_SUSPECTS = 6

TRUE_CLUE = "pista"
FALSE_CLUE = "falsa_pista"


@dataclass
class Suspect:
    name: str
    relation: str
    motive: str
    alibi: str
    secret: str
    alibi_holds: bool
    is_culprit: bool


@dataclass
class Clue:
    kind: str  # TRUE_CLUE ou FALSE_CLUE
    text: str
    points_to: str
    explanation: str = ""


@dataclass
class Case:
    seed: int
    title: str
    era: str
    place: str
    victim_name: str
    victim_occupation: str
    weapon: str
    location: str
    twist: str
    suspects: List[Suspect]
    clues: List[Clue]

    @property
    def culprit(self) -> Suspect:
        return next(s for s in self.suspects if s.is_culprit)


def _gendered(pair: Tuple[str, str], gender: str) -> str:
    return pair[0] if gender == "m" else pair[1]


def _make_people(rng: random.Random, count: int) -> List[Tuple[str, str]]:
    pools = {g: list(names) for g, names in data.FIRST_NAMES.items()}
    surnames = rng.sample(data.SURNAMES, count)
    people = []
    for surname in surnames:
        gender = rng.choice(("m", "f"))
        first = pools[gender].pop(rng.randrange(len(pools[gender])))
        people.append((f"{first} {surname}", gender))
    return people


def generate_case(seed: Optional[int] = None, num_suspects: int = 4) -> Case:
    """Gera um caso. A mesma seed e o mesmo número de suspeitos dão o mesmo caso."""
    if not MIN_SUSPECTS <= num_suspects <= MAX_SUSPECTS:
        raise ValueError(
            f"num_suspects deve estar entre {MIN_SUSPECTS} e {MAX_SUSPECTS}"
        )
    if seed is None:
        seed = random.SystemRandom().randrange(1, 1_000_000)
    rng = random.Random(seed)

    people = _make_people(rng, num_suspects + 1)
    victim_name, victim_gender = people[0]
    victim_occupation = _gendered(rng.choice(data.OCCUPATIONS), victim_gender)

    relations = rng.sample(data.RELATIONS, num_suspects)
    motives = rng.sample(data.MOTIVES, num_suspects)
    alibis = rng.sample(data.ALIBIS, num_suspects)
    culprit_index = rng.randrange(num_suspects)
    secrets = iter(rng.sample(data.SECRETS, num_suspects - 1))

    suspects: List[Suspect] = []
    for i, (name, gender) in enumerate(people[1:]):
        is_culprit = i == culprit_index
        suspects.append(
            Suspect(
                name=name,
                relation=_gendered(relations[i], gender),
                motive=motives[i],
                alibi=alibis[i],
                secret=data.CULPRIT_SECRET if is_culprit else next(secrets),
                alibi_holds=not is_culprit,
                is_culprit=is_culprit,
            )
        )
    culprit = suspects[culprit_index]

    weapon, weapon_clue = rng.choice(data.WEAPONS)
    location, location_clue = rng.choice(data.LOCATIONS)
    generic_clue = rng.choice(data.CULPRIT_CLUES)

    clues = [
        Clue(TRUE_CLUE, text.format(culprit=culprit.name), culprit.name)
        for text in (weapon_clue, location_clue, generic_clue)
    ]

    others = [s for s in suspects if not s.is_culprit]
    herring_count = min(3, len(others))
    for suspect, template in zip(
        rng.sample(others, herring_count),
        rng.sample(data.RED_HERRINGS, herring_count),
    ):
        clues.append(
            Clue(
                FALSE_CLUE,
                template.format(suspect=suspect.name),
                suspect.name,
                f"{suspect.name} {suspect.secret}, e por isso agiu de forma suspeita.",
            )
        )
    rng.shuffle(clues)

    first, surname = victim_name.split()
    title = rng.choice(data.TITLES).format(first=first, surname=surname)

    return Case(
        seed=seed,
        title=title,
        era=rng.choice(data.ERAS),
        place=rng.choice(data.PLACES),
        victim_name=victim_name,
        victim_occupation=victim_occupation,
        weapon=weapon,
        location=location,
        twist=rng.choice(data.TWISTS),
        suspects=suspects,
        clues=clues,
    )
