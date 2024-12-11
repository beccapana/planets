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

# Задание планет и их свойств
planets = [
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
        "pos": [100, 200],
        "radius": 20,
        "color": random_color(),
        "velocity": [0, 0],
        "trail": []
    }
]

# Вспомогательные переменные
selected_planet = None
mouse_attract = [False, False, False]
running = True
clock = pygame.time.Clock()

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

    # Управление выделением планет и их перемещением
    for i in range(NUM_PLANETS):
        if keys[pygame.K_1 + i]:
            selected_planet = i
            if mouse_pressed[0]:
                mouse_attract[i] = True
            if keys[pygame.K_q]:
                planets[i]["pos"] = list(mouse_pos)
                planets[i]["trail"] = []  # Сброс следа
        else:
            mouse_attract[i] = False

    # Обновление скорости планет на основе гравитационного взаимодействия
    if mouse_pressed[2]:
        for i, planet_a in enumerate(planets):
            force_x, force_y = 0, 0

            # Гравитация между планетами
            for j, planet_b in enumerate(planets):
                if i != j:
                    dist = distance(*planet_a["pos"], *planet_b["pos"]) / 100
                    if dist > 1.55:
                        force = SPEED / square(dist)
                        force_x += force * (planet_b["pos"][0] - planet_a["pos"][0]) / dist
                        force_y += force * (planet_b["pos"][1] - planet_a["pos"][1]) / dist

            # Притяжение к мыши, если активно
            if mouse_attract[i]:
                dist = distance(*planet_a["pos"], *mouse_pos) / 100
                if dist > 1.55:
                    force = SPEED / square(dist)
                    force_x += force * (mouse_pos[0] - planet_a["pos"][0]) / dist
                    force_y += force * (mouse_pos[1] - planet_a["pos"][1]) / dist

            # Обновление скорости
            planet_a["velocity"][0] += force_x
            planet_a["velocity"][1] += force_y

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
