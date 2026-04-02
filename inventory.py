import logger
import models  


def use_amulet(inventory: list[str]) -> bool:
    if "амулет" in inventory:
        choice = logger.get_input(
            "Использовать амулет чтобы переиграть событие - 1, продолжить - 2:",
            ["1", "2"],
        )
        if choice == "1":
            inventory.remove("амулет")
            logger.get_achieve("Второе дыхание")
            return True
    return False


def check_amulet(inventory: list[str]) -> None: # дается 1 на каждый мир при сложности новичок 
    if models.game.difficulty == 1 and "амулет" not in inventory:
        inventory.append("амулет")


def show_inventory(inventory: list[str]) -> None:
    logger.wprint(
        "Выберите предмет из инвентаря, чтобы использовать его \n"
        " кроме амулета, он может понадобиться вам в экстренной ситуации "
    )
    for i, item in enumerate(inventory, start=1):
        logger.wprint(f"{i}. {item} ")
