
inventory = {
    1: ['фонарик'],
    2: ['фонарик', 'компас'],
    3: ['фонарик', 'компас', 'амулет'], 
}
worlds = {
    1: "Clé 1: MIROH",
    2: "NOEASY",
    3: "5‑STAR"
}
game = {
    "errors": 0,
    "rudeness_count": 0,
    "kindness":0,
    "input_resets": 0,
    "inventory":[],
    "achievements":[],
    "symbols":{}
}

def get_input( # считает сколько раз игрок решил вводить не то что его попросили. используется вместо input.
        prompt: str,# вводим фразу которую выведет на экран
        options:list[str] #  варианты ответов
        ): 
    while True:
        ans = input(prompt)
        if ans in options:
            return ans
        game['errors'] += 1
        print("Некорректный ввод")
        if game['errors'] >= 3:
            print("Попробуй читать глазами")
            game['input_resets'] += 1
            if game['input_resets'] == 3:
                get_achieve('Да ты издеваешься над нами!!')
            game['errors'] = 0


def use_amulet(inventory: list[str]) -> bool:
    if 'амулет' in inventory:
        choise = get_input('Использовать амулет чтобы переиграть событие - 1, продолжить - 2 ', ['1','2'])
        if choise == '1':
            inventory.remove('амулет')
            get_achive('Второе дыхание')
            return True
    return False


def show_inventory(inventory: list[str]) -> None:
    print("Выберете предмет из инвентаря, чтобы использовать его \n"
    " кроме амулета, он может только откатить время назад")
    for i, item in enumerate(inventory, start=1):
        print(f"{i}. {item}")

def get_achieve(name: str) -> None:
    if name not in game['achievements']:
        print(f"Достижение получено: {name}")
        game['achievements'].append(name)

def fight_with_robot() ->bool: 
    # драка с роботом, правильная комбинация 1 2 3. 
    # количества урона которое можно впитать 3
    print('Вы столкнулись с роботом. Он настроен недружелюбно.\n'
          ' Чтобы пройти испытание, атакуйте(1), блокируйте(2) и уварачивайтесь(3) . \n'
          '  -начать')
    damage = 0
    expected = ['1','2','3']
    step = 0
    while damage < 3 and step < 3:
        action = get_input("Выберете действие 1-3",['1','2','3'])
        if action == expected[step]:
            step += 1
        else:
            damage += 1
            step = 0
    if damage == 3:
        return False
    else:
        return True
    
def sprint()->bool: 
    # иммитирует попытку пробежать незамеченным, 
    # правильный порядок 1 2
    print("Пробегите и не попадите под лучи сканера. \n" \
    " Пригнитесь и перекатитесь, чтобы пройти испытание. \n " \
    "- начать")
    for step in range(2):
        dodge = get_input(f"Введите {step + 1} действие: ",['1','2'])
        if dodge != str(step + 1):
            return False
  
    return True

def miroh_world_act1(inventory:list)-> bool: # расписан шаг 1
    print("\n Вы видите приближающегося робота. Нужно быстро решить, что делать: \n " \
    "1. Спрятаться в мусорном баке \n " \
    "2. Быстро пробежать вперёд.\n" \
    "3.Использовать предмет из инвентаря. ")
    move = get_input("Введите число от 1 до 3",['1','2','3'])
    if int(move) == 1:
        print("Вы тихо сидите, робот проходит мимо.\n Вы теряете время, но остаётесь незамеченным")
        return True
    elif int(move) == 2:
        if sprint():
            print("Вы проскочили и идете дальше")
            return True
        if use_amulet(inventory):
            if sprint():
                print("Вы проскочили и идете дальше")
                return True
        if fight_with_robot():
            print("робот уничтожен, но шум привлекает других;" \
            "\n вы теряете время, но проходите дальше")
            game['rudeness_count'] += 1
            return True
        if use_amulet(inventory):
            if fight_with_robot():
                print("робот уничтожен, но шум привлекает других;" \
                "\n вы теряете время, но проходите дальше")
                game['rudeness_count'] += 1
                return True
        return False
    elif int(move) == 3:
        show_inventory(inventory)
        item = get_input("Введите номер предмета ",[str(i) for i in range(1,len(inventory) + 1)])
        selected_item = inventory[int(item) - 1]
        if selected_item == 'фонарик':
            print('Вы ослепили робота и спокойно прошли')
            return True
        elif selected_item == 'компас':
            print('Вы замираете неподвижно, робот уходит.\n  По компасу вы находите другой маршрут')
            return True
        elif selected_item == 'амулет':
            print('Поздравляю, вы возвращаетесь в начало! а ведь это могло спасти вам жизнь..')
            inventory.remove('амулет')
            return False
    return False

def meeting() -> bool:
    #тут я сделал не очень логично. 
    #bool указывает - берем мы беженцев или нет
    print('Вы натыкаетесь на группу испуганных людей,\n'
          'которые тоже пытаются выбраться. Им нужна помощь.')
    choice = get_input('1. Пройти мимо, не обращая внимания\n '
                       '2. Помочь им найти дорогу \n'
                       '3.Обмануть их (сказать, что знаете путь, но на самом деле использовать их как приманку для роботов)',['1','2','3'])
    if choice == '1':
        return False
    elif choice == '2':
        print('Вы тратите время, но помогаете людям.')
        game['kindness'] += 1
        get_achieve('do u know da way?')
        return True
    elif choice == '3':
        print('Вы обманываете беженцев, они отвлекают роботов, \n '
              'а вы проскальзываете. Вы проходите дальше,\n '
              'но совесть нечиста')
        game['rudeness_count'] += 1
        return False

def check_match(user_way:str, right_way:str) -> bool:
    matche = 0
    for i in range(len(right_way)):
        if user_way[i] == right_way[i]:
            matche += 1
    if matche >= len(right_way) * 0.8:
        return True
    return False

def miroh_world_act2(inventory:list) -> bool: 
    # второй шаг
    # выход из лабиринта 12321
    print('Вы проходите дальше и попадаете в лабиринт. \n '
          ' Чтобы выбраться из него, вам нужно повернуть налево, затем пройти прямо, \n '
          'свернуть направо, снова пройти прямо прямо, и повернуть налево')
    road = ''
    steps = 0
    result = False
    while steps < 5:
        step_choice = get_input('куда пойдёте? \n'
                                '1 - налево \n '
                                '2 - прямо \n '
                                '3 - направо ', ['1','2','3'])
        road += step_choice
        steps += 1
        if steps == 3:
            result = meeting()
            print('После встречи с беженцами вы проходите оставшиеся перекрёстки')
    if road == '12321':
        return True
    elif result and check_match(road,'12321'):
        return True
    return False
         

def miroh_world(inventory:list):
    tries = 1
    print("Вы вступили в мир «Clé 1: MIROH» – Лабиринт улиц.\n"
          " Шумный мегаполис, но  вместо людей улицы патрулируют роботы-надзиратели.\n"
          " Вы чувствуете себя  беглецом, пытающимся пробраться через лабиринт переулков,\n"
          " не попадаясь на \n глаза системе. Где-то здесь прячутся другие беженцы – такие же,\n "
          " как вы, потерянные души, ищущие выход к свободе...\n")
    print("\n Вы входите в темный переулок. Система слежки активирована. \n"
          " Ваша цель – добраться до выхода из этого района, избегая встреч с роботами.")
    act1_end = miroh_world_act1(inventory)
    if not act1_end:
        tries -=1
        if tries > 0:
            act1_att2_end = miroh_world_act1(inventory)
            if not act1_att2_end:
                return False
        else:
            return False
    

    act2_end = miroh_world_act2(inventory)
    if not act2_end:
        tries -=1
        if use_amulet(inventory):
            tries += 1
        if tries > 0:
            act2_att2_end = miroh_world_act2(inventory)
            if not act2_att2_end:
                return False
        else:
            return False
    return True
    

def noeasy_world(inventory:list):
    tries = 1
    pass


def star_world(inventory:list):
    tries = 1
    pass


def main():
    print('Добро пожаловать в игру «Stray Kids: Сновидец SKZ-Verse»!\n'
          ' Выберите уровень сложности: \n '
          ' 1 - "Мастер слов" \n'
          ' 2 - "Преданный STAY" \n'
          ' 3 - "Новичок"\n ')
    difficulty = get_input("Введите уровень сложности: 1-3", ['1','2','3'])
    game['inventory'] = inventory[int(difficulty)].copy()
    print("Благодаря выбранной сложности при себе вы имеете:")
    print(*game['inventory'], sep=', ')
    unused_worlds = [
        "1 — «Clé 1: MIROH» (Лабиринт улиц, где нужно найти выход из хаоса)",
        "2 — «NOEASY» (Мир шума, где ваш голос становится оружием)",
        "3 — «5‑STAR» (Звёздный мир, где решается ваша уникальность)"]
    n = 0
    while n < 3:
        print("Вы засыпаете и попадаете в SKZ‑Verse. Перед вами три мира: \n")
        for world_type in unused_worlds:
                print(world_type)     
        world = get_input("Введите номер мира: ", [str(i) for i in range(1,len(unused_worlds) + 1)])
        unused_worlds.pop(int(world) - 1)
        worlds.pop(int(world))
        if int(world) == 1:
            result = miroh_world(game['inventory'])
            if result:
                game['symbols']['MIROH'] = True
                print('Вы выбрались из лабиринта! Вы получаете символ MIROH')
        elif int(world) == 2:
            result = noeasy_world(game['inventory'])
        elif int(world) == 3:
            result = star_world(game['inventory'])
        n += 1

main()




