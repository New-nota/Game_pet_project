import logger
import inventory as inventory_utils
import models 
from content_loader import load_json


def use_clue(inventory: list[str], step: int) -> None:
    texts = load_json("content/noeasy.json")
    strong_answers = ["2", "3", "1"]
    rude_answers = ["1", "2", "3"]
    use = logger.get_input("Хотите использовать предмет? \n 1 - да \n 2 - нет:", ["1", "2"])
    if use == "2":
        return None
    inventory_utils.show_inventory(inventory)
    logger.wprint("0 - Ничего (вернуться к ответам)")
    options = [str(i) for i in range(1, len(inventory) + 1)] + ["0"]
    item = logger.get_input("Введите номер:", options)
    if item == "0":
        return None
    selected_item = inventory[int(item) - 1]
    if selected_item == "фонарик":
        logger.wprint(
            texts["tools"]["фонарик"]
        )
        logger.wprint(f"Дух разозлится от ответа {rude_answers[step - 1]}")
        return None
    elif selected_item == "компас":
        logger.wprint(
            texts["tools"]["компас"]
        )
        logger.wprint(f"Дух ждет ответ {strong_answers[step - 1]}")
        return None
    elif selected_item == "амулет":
        logger.wprint(texts["tools"]["амулет"])
        inventory.remove("амулет")
        models.game.unnecessary_use_amulet_count += 1
        return None


def quiz(inventory: list[str]) -> bool:
    texts = load_json("content/noeasy.json")
    question_pool = texts["quiz"]
    stats = {"strong": 0, "kindness": 0, "rudeness": 0}
    for i, data in enumerate(question_pool, start=1):
        logger.wprint(data["question"])
        for key, answer in data["answers"].items():
            logger.wprint(key, " - ", answer)
        use_clue(inventory, i)
        user_answer = logger.get_input("Введите номер ответа:", ["1", "2", "3"])
        karma = data["scores"][user_answer]
        for stat, value in karma.items():
            stats[stat] += value
    models.game.rudeness_count += stats["rudeness"]
    models.game.kindness_count += stats["kindness"]
    if stats["strong"] >= 2:
        return True
    else:
        if stats["kindness"] == 3:
            logger.get_achieve("Absolute Karma, but no sense")
        return False

def noeasy_world(inventory: list[str]) -> bool:
    texts = load_json("content/noeasy.json")
    inventory_utils.check_amulet(inventory)
    logger.wprint(
        texts["noeasy_intro"]
    )
    if not quiz(inventory):
        logger.wprint(
            texts["bad_ends"]["first_end"]
        )
        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            if not quiz(inventory):
                logger.wprint(
                    texts["bad_ends"]["second_end"]
                )
                return False
        else:
            return False
    return True
