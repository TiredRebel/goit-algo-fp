"""
Генератор фракталу "Дерево Піфагора"

Цей модуль створює фрактал "дерево Піфагора" за допомогою рекурсії 
та графічної бібліотеки turtle. Користувач може вказати рівень рекурсії 
як параметр командного рядка або через інтерактивне введення.
"""

import turtle
import math
import sys


def draw_square(side: float) -> None:
    """
    Намалювати квадрат заданого розміру.
    
    Аргументи:
        side: Довжина сторони квадрата
    """
    for _ in range(4):
        turtle.forward(side)
        turtle.left(90)


def pythagorean_tree(side: float, level: int) -> None:
    """
    Намалювати дерево Піфагора за допомогою рекурсії.
    
    Аргументи:
        side: Довжина сторони поточного квадрата
        level: Поточний рівень рекурсії (глибина)
    """
    if level == 0:
        return
    
    # Намалювати поточний квадрат
    draw_square(side)
    
    # Обчислити нову довжину сторони (використовуючи теорему Піфагора)
    new_side = side / math.sqrt(2)
    
    # Зберегти поточну позицію та напрямок
    position = turtle.position()
    heading = turtle.heading()
    
    # Перейти до верхнього лівого кута квадрата
    turtle.forward(side)
    turtle.left(90)
    turtle.forward(side)
    turtle.right(90)
    
    # Зберегти позицію верхнього лівого кута
    top_left = turtle.position()
    top_heading = turtle.heading()
    
    # Намалювати лівий квадрат (під кутом 45 градусів вліво)
    turtle.left(45)
    pythagorean_tree(new_side, level - 1)
    
    # Повернутися до верхнього лівого кута
    turtle.penup()
    turtle.goto(top_left)
    turtle.setheading(top_heading)
    turtle.pendown()
    
    # Перейти до верхнього правого кута
    turtle.forward(side)
    
    # Намалювати правий квадрат (під кутом 45 градусів вправо)
    turtle.right(45)
    pythagorean_tree(new_side, level - 1)
    
    # Повернутися до початкової позиції
    turtle.penup()
    turtle.goto(position)
    turtle.setheading(heading)
    turtle.pendown()


def calculate_initial_side(level: int, screen_height: int = 900) -> float:
    """
    Обчислити оптимальний розмір початкового квадрата залежно від рівня рекурсії.
    
    Аргументи:
        level: Рівень рекурсії
        screen_height: Висота екрану в пікселях
    
    Повертає:
        Оптимальна довжина сторони початкового квадрата
    """
    # Приблизна висота дерева розраховується як сума геометричної прогресії
    # Висота ≈ side * (1 + sqrt(2) + sqrt(2)^2 + ... + sqrt(2)^(level-1))
    # Це приблизно side * (sqrt(2)^level - 1) / (sqrt(2) - 1)
    
    if level <= 0:
        return 100
    
    # Коефіцієнт для безпечного відступу від країв екрану
    safety_factor = 0.4
    usable_height = screen_height * safety_factor
    
    # Обчислюємо оптимальний розмір
    height_ratio = (math.sqrt(2) ** level - 1) / (math.sqrt(2) - 1)
    initial_side = usable_height / height_ratio
    
    # Обмежуємо мінімальний та максимальний розмір
    initial_side = max(10, min(initial_side, 200))
    
    return initial_side


def setup_screen(width: int = 1400, height: int = 900) -> None:
    """
    Налаштувати параметри екрану для малювання.
    
    Аргументи:
        width: Ширина екрану в пікселях
        height: Висота екрану в пікселях
    """
    screen = turtle.Screen()
    screen.setup(width, height)
    screen.title("Дерево Піфагора - Фрактал")
    screen.bgcolor("white")
    turtle.speed(0)  # Найшвидша швидкість малювання
    turtle.hideturtle()


def get_recursion_level() -> int:
    """
    Отримати рівень рекурсії від користувача через командний рядок 
    або інтерактивне введення.
    
    Повертає:
        Рівень рекурсії (невід'ємне ціле число)
    """
    # Спробувати отримати рівень з аргументів командного рядка
    if len(sys.argv) > 1:
        try:
            level = int(sys.argv[1])
            if level < 0:
                print("Рівень рекурсії має бути невід'ємним числом.")
                print("Використовуємо інтерактивне введення...")
            else:
                print(f"Використовується рівень рекурсії: {level}")
                return level
        except ValueError:
            print("Некоректний аргумент. Використовуємо інтерактивне введення...")
    
    # Інтерактивне введення
    while True:
        try:
            level = int(input("\nВведіть рівень рекурсії (рекомендовано: 1-12): "))
            if level < 0:
                print("Будь ласка, введіть невід'ємне ціле число.")
                continue
            if level > 15:
                print("Увага: Високий рівень може зайняти багато часу!")
            return level
        except ValueError:
            print("Некоректне введення. Будь ласка, введіть ціле число.")


def draw_tree(level: int, initial_side: float = None) -> None:
    """
    Підготувати екран та намалювати дерево Піфагора.
    
    Аргументи:
        level: Рівень рекурсії
        initial_side: Довжина сторони початкового квадрата (якщо None, обчислюється автоматично)
    """
    # Налаштувати екран
    screen_height = 900
    setup_screen(height=screen_height)
    
    # Обчислити оптимальний розмір початкового квадрата
    if initial_side is None:
        initial_side = calculate_initial_side(level, screen_height)
    
    print(f"Розмір початкового квадрата: {initial_side:.1f} пікселів")
    
    # Позиціонувати черепашку в центрі екрану
    # Зміщуємо трохи вниз, щоб дерево мало простір для росту вгору
    vertical_offset = -screen_height * 0.15
    turtle.penup()
    turtle.goto(-initial_side / 2, vertical_offset)
    turtle.setheading(0)  # Напрямок вправо
    turtle.pendown()
    
    # Встановити властивості малювання
    turtle.color("darkred")
    turtle.pensize(1)
    
    # Намалювати дерево Піфагора
    print(f"Починаємо малювання дерева Піфагора з {level} рівнями...")
    pythagorean_tree(initial_side, level)
    
    # Залишити вікно відкритим
    print(f"\nДерево Піфагора з {level} рівнями завершено!")
    print("Клацніть на вікні, щоб закрити.")
    turtle.exitonclick()


def main() -> None:
    """
    Головна функція для запуску генератора фракталу "дерево Піфагора".
    """
    print("=" * 50)
    print("Генератор фракталу 'Дерево Піфагора'")
    print("=" * 50)
    print("\nВикористання:")
    print("  python pythagorean_tree.py [рівень_рекурсії]")
    print("  Приклад: python pythagorean_tree.py 8")
    
    # Отримати рівень рекурсії
    level = get_recursion_level()
    
    # Намалювати дерево
    draw_tree(level)


if __name__ == "__main__":
    main()