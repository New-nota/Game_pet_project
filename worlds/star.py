import logger
import inventory as inventory_utils
from content_loader import load_json
import models 
data = load_json("content/star.json")

def preparation() -> None:
    texts = data["preparation"]
    logger.wprint(
        texts["intro_preparation"]
    )
    for key, value in texts["style_variation"].items():
        logger.wprint(f"{key} - {value}")

    ans = logger.get_input("Введите номер выбранного стиля: ", ["1", "2", "3", "4"])
    chosen_style = texts["style_variation"][ans]
    logger.wprint(
        "Участники зафиксировали твой выбор \n" "Ты выступаешь в стиле ", chosen_style
    )     

def performance_round_1(inventory:list[str]) -> int:
    stars_collected = 0
    texts = data["performance_round_1"]
    logger.wprint(
        texts["performance_round_1_intro"]
    )
    ans = logger.get_input("Введите номер выбранного вами варианта:", ["1", "2", "3", "4"])
    if ans == "4":
        inventory_utils.show_inventory(inventory)
        options = [str(i) for i in range(1, len(inventory) + 1)]
        item = logger.get_input("Введите номер предмета:", options)
        selected_item = inventory[int(item) - 1]
        if selected_item == "фонарик":
            logger.wprint(texts["tools"]["фонарик"])
        elif selected_item == "компас":
            logger.wprint(texts["tools"]["компас"])
        elif selected_item == "амулет":
            logger.wprint(texts["tools"]["амулет"])
            inventory.remove("амулет")
            models.game.unnecessary_use_amulet_count += 1
        logger.wprint(
            texts["choose_style"]
        )
        ans = logger.get_input("Введите номер выбранного вами варианта:", ["1", "2", "3"])
    if ans == "1":
        logger.wprint("Выступление прошло энергично, зрители поддерживают.")
        stars_collected += 1
    elif ans == "2":
        logger.wprint("Копия выглядит бледно, публика чувствует фальшь.")
        models.game.rudeness_count += 1
    elif ans == "3":
        logger.wprint("Вот это и есть стиль 5 STAR!")
        stars_collected += 2
        logger.get_achieve("АШАЛЕТЬ ЧТО ТЫ ТВОРИШЬ!!")
    return stars_collected

def performance_round_2() -> int:
    texts = data["performance_round_2"]
    stars_collected = 0 
    logger.wprint(
        texts
    )
    selected_response = logger.get_input("Введите номер действия:", ["1", "2", "3"])
    if selected_response == "1":
        logger.wprint("Зал реагирует, но чувствуется излишняя агрессия.")
        stars_collected += 1
        models.game.rudeness_count += 1
    elif selected_response == "2":
        logger.wprint("Неуверенность снижает поддержку зала.")

        logger.wprint("Из тишины зала издаётся...")
        logger.get_achieve("HA-HA")
    elif selected_response == "3":
        logger.wprint("Зрители отвечают теплом, поддержка растёт.")
        stars_collected += 2
        models.game.kindness_count += 1
    return stars_collected


def star_world_gameplay(inventory: list[str]) -> bool:
    stars_collected = 0        
    preparation()
    stars_collected += performance_round_1(inventory)
    stars_collected += performance_round_2()
    if stars_collected >= 3:
        return True
    else:
        logger.wprint("Вам не хватило уверенности. Символ не получен.")
        return False

    
def star_world(inventory: list[str]) -> bool:
    texts = data["star_intro"]
    inventory_utils.check_amulet(inventory)
    logger.wprint(
        texts
    )
    result = star_world_gameplay(inventory)
    if not result:
        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            result = star_world_gameplay(inventory)
            if not result:
                return False
        else:
            return False
    return True
