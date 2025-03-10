import pygame
import math
import random

# Константы
WIDTH, HEIGHT = 1920, 1080  # Полный размер экрана
SPEED = 0.1
NUM_PLANETS = 5
TRAIL_LENGTH = 200
G_CONSTANT = 5.0  # Усиленная гравитационная постоянная для взаимодействия планет

# Функции
def square(value):
    """Возвращает квадрат числа."""
    return value ** 2

def random_color():
    """Возвращает случайный цвет."""
    return random.randint(40, 200), random.randint(40, 200), random.randint(40, 200)

def distance(x1, y1, x2, y2):
    """Возвращает расстояние между двумя точками."""
    return math.sqrt(square(x2 - x1) + square(y2 - y1))

def create_star():
    """Создание звезды."""
    return {
        "pos": list(pygame.mouse.get_pos()),
        "radius": 30,
        "color": (255, 255, 0)
    }

def create_black_hole():
    """Создание черной дыры."""
    return {
        "pos": list(pygame.mouse.get_pos()),
        "radius": 100,
        "color": (112, 128, 144),
        "event_horizon": 100  # Горизонт событий
    }

def create_random_planet():
    """Создание планеты с случайным положением и цветом."""
    return {
        "pos": [random.randint(0, WIDTH), random.randint(0, HEIGHT)],
        "radius": 20,
        "color": random_color(),
        "velocity": [0, 0],
        "mass": random.uniform(1, 5),  # Масса планеты
        "trail": []
    }

def reset_planets():
    """Сбрасывает планеты к начальному состоянию."""
    global planets, star, black_hole
    planets = [create_random_planet() for _ in range(NUM_PLANETS)]
    star = None
    black_hole = None

def draw_black_hole_effect(black_hole, screen):
    """Рисует эффект гравитации вокруг черной дыры."""
    for i in range(1, 20):
        alpha = max(0, 255 - i * 12)
        color = (112, 128, 144, alpha)
        radius = black_hole["radius"] + i * 5
        pygame.draw.circle(screen, (112, 128, 144), black_hole["pos"], radius, width=1)

# Инициализация pygame
pygame.init()

# Настройка окна с рамками и полноэкранным режимом
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.NOFRAME)
pygame.display.set_caption("Planets Simulation")

# Задание начальных планет и их свойств
reset_planets()

# Управляющие объекты и параметры
star = None  # Звезда
black_hole = None  # Черная дыра
current_mode = 1  # Режим: 1 - зажатие мыши, 2 - звезда, 3 - черная дыра
running = True
clock = pygame.time.Clock()

# Главный цикл
while running:
    screen.fill((0, 0, 0))  # Очистка экрана

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_planets()

    keys = pygame.key.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # Управление режимами
    if keys[pygame.K_1]:
        current_mode = 1
        star = None
        black_hole = None
    elif keys[pygame.K_2]:
        current_mode = 2
        if not star:
            star = create_star()
    elif keys[pygame.K_3]:
        current_mode = 3
        if not black_hole:
            black_hole = create_black_hole()

    # Режим 1: Притяжение к мыши с зажатой кнопкой
    if current_mode == 1 and mouse_pressed[2]:
        for planet in planets:
            dist = distance(*planet["pos"], *mouse_pos) / 100
            if dist > 1.55:
                force = SPEED / square(dist)
                planet["velocity"][0] += force * (mouse_pos[0] - planet["pos"][0]) / dist
                planet["velocity"][1] += force * (mouse_pos[1] - planet["pos"][1]) / dist

    # Режим 2: Звезда с притяжением
    if current_mode == 2 and star:
        star["pos"] = mouse_pos
        for planet in planets:
            dist = distance(*planet["pos"], *star["pos"]) / 100
            if dist > 1.55:
                force = SPEED / square(dist)
                planet["velocity"][0] += force * (star["pos"][0] - planet["pos"][0]) / dist
                planet["velocity"][1] += force * (star["pos"][1] - planet["pos"][1]) / dist
        pygame.draw.circle(screen, star["color"], star["pos"], star["radius"])

    # Режим 3: Черная дыра
    if current_mode == 3 and black_hole:
        black_hole["pos"] = mouse_pos
        draw_black_hole_effect(black_hole, screen)
        for planet in planets[:]:
            dx, dy = black_hole["pos"][0] - planet["pos"][0], black_hole["pos"][1] - planet["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)

            if dist < black_hole["event_horizon"]:
                # Эффект приливных сил
                planet["radius"] -= 0.2
                if planet["radius"] <= 0:
                    planets.remove(planet)
                    continue

            dist_scaled = dist / 100
            if dist_scaled > 1.55:
                force = SPEED * 5 / square(dist_scaled)
                planet["velocity"][0] += force * dx / dist
                planet["velocity"][1] += force * dy / dist

            # Искривление траектории: гравитационный манёвр
            angle = math.atan2(dy, dx)
            velocity_angle = math.atan2(planet["velocity"][1], planet["velocity"][0])
            angle_diff = angle - velocity_angle
            planet["velocity"][0] += G_CONSTANT * math.sin(angle_diff)
            planet["velocity"][1] += G_CONSTANT * math.cos(angle_diff)

    # Взаимодействие планет друг с другом
    for i, planet1 in enumerate(planets):
        for planet2 in planets[i + 1:]:
            dx, dy = planet2["pos"][0] - planet1["pos"][0], planet2["pos"][1] - planet1["pos"][1]
            dist = distance(*planet1["pos"], *planet2["pos"])
            if dist > 0 and dist < 200:  # Условие для гравитационного взаимодействия
                force = G_CONSTANT * planet1["mass"] * planet2["mass"] / square(dist)
                planet1["velocity"][0] += force * dx / dist / planet1["mass"]
                planet1["velocity"][1] += force * dy / dist / planet1["mass"]
                planet2["velocity"][0] -= force * dx / dist / planet2["mass"]
                planet2["velocity"][1] -= force * dy / dist / planet2["mass"]

    # Обновление позиций планет
    for planet in planets:
        planet["pos"][0] += planet["velocity"][0] / 100
        planet["pos"][1] += planet["velocity"][1] / 100
        planet["trail"].append(tuple(planet["pos"]))
        if len(planet["trail"]) > TRAIL_LENGTH:
            planet["trail"].pop(0)

    # Рендеринг
    for planet in planets:
        for point in planet["trail"]:
            pygame.draw.circle(screen, (255, 255, 255), (int(point[0]), int(point[1])), 3)

        pygame.draw.circle(screen, planet["color"], (int(planet["pos"][0]), int(planet["pos"][1])), int(planet["radius"]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()