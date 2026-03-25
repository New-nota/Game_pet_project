import models 
import sys

LOG_FILE = "gameplay.txt"


def _safe_console_text(text: str) -> str:
    encoding = sys.stdout.encoding or "utf-8"
    try:
        text.encode(encoding)
        return text
    except UnicodeEncodeError:
        return text.encode(encoding, errors="replace").decode(encoding)


def reset_log() -> None:
    with open(LOG_FILE, "w", encoding="utf-8"):
        pass


def wprint(*to_file) -> None:
    output_parts = []
    for item in to_file:
        if isinstance(item, list): # проверка является ли item списком
            output_parts.append(", ".join(map(str,item)))
        else:
            output_parts.append(str(item))
    text = " ".join(output_parts)
    print(_safe_console_text(text))
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def get_input(  # считает сколько раз игрок решил вводить не то что его попросили. используется вместо input.
    prompt: str,  # вводим фразу которую выведет на экран
    options: list[str],  #  варианты ответов
) -> str:
    while True:
        wprint(prompt)
        ans = input().strip()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(ans + "\n")
        if ans in options:
            return ans
        models.game.errors += 1
        wprint("Некорректный ввод")
        if models.game.errors >= 3:
            wprint("Попробуй читать глазами")
            models.game.input_resets += 1
            if models.game.input_resets == 3:
                get_achieve("Да ты издеваешься над нами!!")
            models.game.errors = 0


def get_achieve(name: str) -> None:
    if name not in models.game.achievements:
        wprint(f"Достижение получено: {name}")
        models.game.achievements.append(name)
