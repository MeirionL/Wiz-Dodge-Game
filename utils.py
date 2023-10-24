from pathlib import Path

from pygame.font import SysFont
from pygame.image import load
from pygame.transform import scale


def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()


def draw_text(text):
    font = SysFont("comicsans", 30)
    screen_text = font.render(text, 1, "white")
    return screen_text


def save_score(score):
    with open("assets/data/highscore.txt", "w") as file:
        file.write(str(score))


def load_score():
    try:
        with open("assets/data/highscore.txt", "r") as file:
            score = float(file.read())
            return score
    except FileNotFoundError:
        score = 0.0
        return score


def place_cannons():
    cannon_image_details = [
        ("cannon_img_down", (50, 50)),
        ("cannon_img_left", (50, 50)),
        ("cannon_img_up", (50, 50)),
        ("cannon_img_right", (50, 50)),
    ]
    cannon_positions = [
        (225, 25),
        (275, 25),
        (325, 25),
        (525, 225),
        (525, 275),
        (525, 325),
        (225, 525),
        (275, 525),
        (325, 525),
        (25, 225),
        (25, 275),
        (25, 325),
    ]
    cannon_tuples = []
    for i in range(len(cannon_positions)):
        cannon_direction, cannon_size = cannon_image_details[i // 3]
        cannon_image = scale(load_sprite(cannon_direction, True), cannon_size)
        cannon_tuples.append((cannon_image, cannon_positions[i]))
    return cannon_tuples
