"""NoirForge: gerador de casos de ficção policial, por OctoCorsair Labs."""

from .generator import Case, Clue, Suspect, generate_case

__version__ = "1.0.0"
__all__ = ["Case", "Clue", "Suspect", "generate_case", "__version__"]
