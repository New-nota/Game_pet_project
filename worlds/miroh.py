import logger
import inventory as inventory_utils
from content_loader import load_json
import models 
data = load_json("content/miroh.json")

def fight_with_robot() -> bool:
    texts = data["miroh_act_1"]["choosed_2"]
    # драка с роботом, правильная комбинация 1 2 3.
    # количества урона которое можно впитать 3
    logger.wprint(
        texts["robot_intro"]
    )
    damage = 0
    expected = ["1", "2", "3"]
    step = 0
    while damage < 3 and step < 3:
        action = logger.get_input("Выберите действие 1-3: ", ["1", "2", "3"])
        if action == expected[step]:
            step += 1
        else:
            damage += 1
            step = 0
    if damage == 3:
        return False
    else:
        return True


def sprint() -> bool:
    texts = data["miroh_act_1"]["choosed_2"]
    # имитирует попытку пробежать незамеченным,
    # правильный порядок 1 2
    logger.wprint(
        texts["sprint_intro"]
    )
    for step in range(2):
        dodge = logger.get_input(f"Введите {step + 1} действие: ", ["1", "2"])
        if dodge != str(step + 1):
            return False

    return True


def miroh_world_act1(inventory: list[str]) -> bool:  # расписан шаг 1
    texts = data["miroh_act_1"]
    logger.wprint(
        texts["choose_move_text"]
    )
    move = logger.get_input("Введите число от 1 до 3:", ["1", "2", "3"])
    if move == "1":
        logger.wprint(
            texts["choosed_1"]
        )
        return True
    elif move == "2":
        if sprint():
            logger.wprint(texts["choosed_2"]["sucsessfull_sprint"])
            return True
        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            if sprint():
                logger.wprint(texts["choosed_2"]["sucsessfull_sprint"])
                return True
        if fight_with_robot():
            logger.wprint(
                texts["choosed_2"]["robot_defeated"]
            )
            models.game.rudeness_count += 1
            return True
        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            if fight_with_robot():
                logger.wprint(
                    texts["choosed_2"]["robot_defeated"]
                )
                models.game.rudeness_count += 1
                return True
        logger.wprint(texts["choosed_2"]["robot_wins"])
        return False
    elif move == "3":
        inventory_utils.show_inventory(inventory)
        item = logger.get_input(
            "Введите номер предмета:", [str(i) for i in range(1, len(inventory) + 1)]
        )
        selected_item = inventory[int(item) - 1]
        if selected_item == "фонарик":
            logger.wprint(texts["choosed_3"]["tools"]["фонарик"])
            return True
        elif selected_item == "компас":
            logger.wprint(
                texts["choosed_3"]["tools"]["компас"]
            )
            return True
        elif selected_item == "амулет":
            logger.wprint(
                texts["choosed_3"]["tools"]["амулет"]
            )
            inventory.remove("амулет")
            models.game.unnecessary_use_amulet_count += 1
            return True
    return False


def meeting() -> bool: # здесь True - флаг того что мы взяли беженцев, False - то что они не с нами
    texts = data["miroh_act_2"]
    logger.wprint(
        texts["meeting_intro"]
    )
    choice = logger.get_input(
        str(texts["meeting_choose"]),
        ["1", "2", "3"],
    )
    if choice == "1":
        return False
    elif choice == "2":
        logger.wprint("Вы тратите время, но помогаете людям.")
        models.game.kindness_count += 1
        logger.get_achieve("do u know da way?")
        return True
    elif choice == "3":
        logger.wprint(
            texts["choosed_lie"]
        )
        models.game.rudeness_count += 1
        return False


def check_match(user_way: str, right_way: str) -> bool:
    matches = 0
    for i in range(len(right_way)):
        if user_way[i] == right_way[i]:
            matches += 1
    if matches >= len(right_way) * 0.8:
        return True
    return False


def miroh_world_act2() -> bool:
    texts = data["miroh_act_2"]
    # второй шаг
    # выход из лабиринта 12321
    logger.wprint(
        texts["act_2_intro"]
    )
    road = ""
    steps = 0
    get_group = False
    while steps < 5:
        step_choice = logger.get_input(
            "куда пойдёте? \n" "1 - налево \n " "2 - прямо \n " "3 - направо",
            ["1", "2", "3"],
        )
        road += step_choice
        steps += 1
        if steps == 3:
            get_group = meeting()
            logger.wprint("После встречи с беженцами вы проходите оставшиеся перекрёстки")
    if road == "12321":
        return True
    elif get_group and check_match(road, "12321"):
        return True
    logger.wprint("К сожалению вы потерялись в лабиринте")
    return False


def miroh_world(inventory: list[str]) -> bool:
    texts = data
    inventory_utils.check_amulet(inventory)
    logger.wprint(
        texts["intro_miroh"]
    )
    act1_end = miroh_world_act1(inventory)
    if not act1_end:

        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            act1_att2_end = miroh_world_act1(inventory)
            if not act1_att2_end:
                return False
        else:
            return False

    act2_end = miroh_world_act2()
    if not act2_end:
        if inventory_utils.use_amulet(inventory):
            models.game.used_amulet += 1
            act2_att2_end = miroh_world_act2()
            if not act2_att2_end:
                return False
        else:
            return False
    return True
