import worlds.miroh
import worlds.noeasy
import worlds.star
import logger
import models 
from content_loader import load_json
 
def determine_ending() -> tuple[str, str]:
    texts = load_json("content/engine.json")["endings"]
    symbols_count = len(models.game.symbols)
    total_amulet_uses = (
        models.game.used_amulet + models.game.unnecessary_use_amulet_count
    )
    if symbols_count == 3 and models.game.unnecessary_use_amulet_count == 3:
        return ("награди себя сам...", texts["награди себя сам..."])
    elif symbols_count == 3:
        return (
           "GOLDEN STAY", texts["GOLDEN STAY"]
        )
    elif models.game.kindness_count >= 4:
        return (
            "THE KEEPER OF DREAMS", texts["THE KEEPER OF DREAMS"]
        )
    elif total_amulet_uses >= 2:
        return (
            "С первого раза!(почти)", texts["С первого раза!(почти)"]
        )
    elif symbols_count == 2:
        return (
            "GOOD FAN", texts["GOOD FAN"]
        )
    elif symbols_count == 1:
        return (
            "THE DREAMER", texts["THE DREAMER"]
        )
    elif symbols_count == 0 and models.game.rudeness_count >= 4:
        return (
           "U TOXIC BTW", texts["U TOXIC BTW"]
        )
    return ("CAPTIVE STAY", texts["CAPTIVE STAY"])


def run_game() -> None:
    texts = load_json("content/engine.json")
    models.reset_game_state()
    logger.reset_log()

    logger.wprint(
        texts["choose_difficulty"]
    )
    difficulty = logger.get_input("Введите уровень сложности:", ["1", "2", "3"])
    models.game.inventory = models.defaults.choose_difficulty[int(difficulty)].copy()
    models.game.difficulty = int(difficulty)
    logger.wprint("Благодаря выбранной сложности при себе вы имеете:")
    logger.wprint(models.game.inventory)
    available_worlds = [
        (1, "«Clé 1: MIROH» (Лабиринт улиц, где нужно найти выход из хаоса)"),
        (2, "«NOEASY» (Мир шума, где ваш голос становится оружием)"),
        (3, "«5‑STAR» (Звёздный мир, где решается ваша уникальность)"),
    ]
    selected_inventory = models.game.inventory
    logger.wprint("Вы засыпаете и попадаете в SKZ‑Verse. Перед вами три мира:\n")
    while available_worlds:
        for idx, (_, world_type) in enumerate(available_worlds, start=1):
            logger.wprint(f"{idx}. {world_type}")

        world = logger.get_input(
            "Введите номер мира:", [str(i) for i in range(1, len(available_worlds) + 1)]
        )
        world_id, _ = available_worlds.pop(int(world) - 1)

        if world_id == 1:
            result = worlds.miroh.miroh_world(selected_inventory)
            if result:
                models.game.symbols.append("MIROH") 
                logger.wprint("Вы выбрались из лабиринта! Вы получаете символ MIROH")
        elif world_id == 2:
            result = worlds.noeasy.noeasy_world(selected_inventory)
            if result:
                models.game.symbols.append("NOEASY")
                logger.wprint(
                    "Дух исчезает. Вы не поддались на провокации и сохранили внутреннюю уверенность.\n"
                    "Вы получаете символ NOEASY."
                )
        elif world_id == 3:
            result = worlds.star.star_world(selected_inventory)
            if result:
                models.game.symbols.append("5-STAR")
                logger.wprint("Вы получаете символ 5-STAR. Вы показали себя настоящего.\n ")

    ending_name, ending_description = determine_ending()
    logger.get_achieve(ending_name)
    logger.wprint(ending_description)
