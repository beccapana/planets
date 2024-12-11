import pygame
import math
import random

# Константы
WIDTH, HEIGHT = 920, 500
SPEED = 0.1
NUM_PLANETS = 3
TRAIL_LENGTH = 200

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

# Инициализация pygame
pygame.init()

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planets Simulation")

# Задание начальных планет и их свойств
initial_planets = [
    {
        "pos": [100, 20],
        "radius": 20,
        "color": random_color(),
        "velocity": [0, 0],
        "trail": []
    },
    {
        "pos": [100, 200],
        "radius": 20,
        "color": random_color(),
        "velocity": [0, 0],
        "trail": []
    },
    {
        "pos": [100, 300],
        "radius": 20,
        "color": random_color(),
        "velocity": [0, 0],
        "trail": []
    }
]

# Создание копии начальных данных планет
planets = [planet.copy() for planet in initial_planets]

# Управляющие объекты и параметры
star = None  # Звезда
black_hole = None  # Черная дыра
current_mode = 1  # Режим: 1 - зажатие мыши, 2 - звезда, 3 - черная дыра
running = True
clock = pygame.time.Clock()

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
        "radius": 40,
        "color": (0, 0, 0),
        "event_horizon": 100  # Горизонт событий
    }

def reset_planets():
    """Сбрасывает планеты к начальному состоянию."""
    global planets, star, black_hole
    planets = [planet.copy() for planet in initial_planets]
    star = None
    black_hole = None

# Главный цикл
while running:
    screen.fill((0, 0, 0))  # Очистка экрана

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    elif keys[pygame.K_r]:  # Возврат всех планет
        reset_planets()

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
        star["pos"] = mouse_pos  # Звезда следует за мышью
        for planet in planets:
            dist = distance(*planet["pos"], *star["pos"]) / 100
            if dist > 1.55:
                force = SPEED / square(dist)
                planet["velocity"][0] += force * (star["pos"][0] - planet["pos"][0]) / dist
                planet["velocity"][1] += force * (star["pos"][1] - planet["pos"][1]) / dist
        pygame.draw.circle(screen, star["color"], star["pos"], star["radius"])

    # Режим 3: Черная дыра
    if current_mode == 3 and black_hole:
        black_hole["pos"] = mouse_pos  # Черная дыра следует за мышью
        for planet in planets:
            dist = distance(*planet["pos"], *black_hole["pos"])
            if dist < black_hole["event_horizon"]:
                planets.remove(planet)  # Планета поглощена
                continue
            dist_scaled = dist / 100
            if dist_scaled > 1.55:
                force = SPEED * 5 / square(dist_scaled)  # Усиленное притяжение
                planet["velocity"][0] += force * (black_hole["pos"][0] - planet["pos"][0]) / dist
                planet["velocity"][1] += force * (black_hole["pos"][1] - planet["pos"][1]) / dist
        pygame.draw.circle(screen, black_hole["color"], black_hole["pos"], black_hole["radius"])

    # Обновление позиций планет
    for planet in planets:
        planet["pos"][0] += planet["velocity"][0] / 100
        planet["pos"][1] += planet["velocity"][1] / 100

        # Добавление позиции в след
        planet["trail"].append(tuple(planet["pos"]))
        if len(planet["trail"]) > TRAIL_LENGTH:
            planet["trail"].pop(0)

    # Рендеринг
    for planet in planets:
        # Рисование следа
        for point in planet["trail"]:
            pygame.draw.circle(screen, (255, 255, 255), (int(point[0]), int(point[1])), 3)

        # Рисование планеты
        pygame.draw.circle(screen, planet["color"], (int(planet["pos"][0]), int(planet["pos"][1])), planet["radius"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
