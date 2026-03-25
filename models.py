from dataclasses import dataclass, field

@dataclass
class GameState:
    errors: int = 0
    rudeness_count: int  = 0
    kindness_count: int = 0
    input_resets: int = 0
    difficulty: int = 0
    unnecessary_use_amulet_count: int = 0
    used_amulet: int = 0
    inventory: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)

game = GameState()


@dataclass
class GameDefaults:
    choose_difficulty: dict[int, list[str]] = field(
        default_factory=lambda:{
        1: ["фонарик"],
        2: ["фонарик", "компас"],
        3: ["фонарик", "компас", "амулет"],
        }
    )


defaults = GameDefaults()


def reset_game_state() -> None:
    game.errors = 0
    game.rudeness_count = 0
    game.kindness_count = 0
    game.input_resets = 0
    game.difficulty = 0
    game.unnecessary_use_amulet_count = 0
    game.used_amulet = 0
    game.inventory.clear()
    game.achievements.clear()
    game.symbols.clear()
