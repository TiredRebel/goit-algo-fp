"""
Модуль для розв'язання задачі вибору їжі з максимальною калорійністю.

Реалізує два підходи:
- Жадібний алгоритм (greedy algorithm)
- Динамічне програмування (dynamic programming)
"""

from typing import Dict, List, Tuple


# Дані про їжу
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


def greedy_algorithm(
    items: Dict[str, Dict[str, int]],
    budget: int
) -> Dict[str, int]:
    """
    Жадібний алгоритм для вибору страв з максимальною калорійністю.

    Вибирає страви на основі найкращого співвідношення калорій до вартості,
    не перевищуючи заданий бюджет.

    Args:
        items: Словник страв з вартістю та калорійністю.
        budget: Доступний бюджет.

    Returns:
        Dict[str, int]: Словник вибраних страв та їх кількості.
    """
    # Обчислюємо співвідношення калорій до вартості
    ratios: List[Tuple[str, float]] = []
    for name, info in items.items():
        ratio = info["calories"] / info["cost"]
        ratios.append((name, ratio))
    
    # Сортуємо за співвідношенням (від найкращого до найгіршого)
    ratios.sort(key=lambda x: x[1], reverse=True)
    
    selected: Dict[str, int] = {}
    remaining_budget = budget
    
    # Жадібно вибираємо страви
    for name, _ in ratios:
        cost = items[name]["cost"]
        # Визначаємо скільки разів можемо купити цю страву
        quantity = remaining_budget // cost
        
        if quantity > 0:
            selected[name] = quantity
            remaining_budget -= quantity * cost
    
    return selected


def dynamic_programming(
    items: Dict[str, Dict[str, int]],
    budget: int
) -> Dict[str, int]:
    """
    Алгоритм динамічного програмування для оптимального вибору страв.

    Обчислює оптимальний набір страв для максимізації калорійності
    при заданому бюджеті.

    Args:
        items: Словник страв з вартістю та калорійністю.
        budget: Доступний бюджет.

    Returns:
        Dict[str, int]: Словник вибраних страв та їх кількості.
    """
    # Створюємо список страв
    item_list = list(items.keys())
    
    # Таблиця для динамічного програмування
    # dp[w] = максимальна калорійність при бюджеті w
    dp: List[int] = [0] * (budget + 1)
    # Зберігаємо інформацію про вибір
    choices: List[Dict[str, int]] = [{} for _ in range(budget + 1)]
    
    # Заповнюємо таблицю
    for w in range(1, budget + 1):
        for item_name in item_list:
            cost = items[item_name]["cost"]
            calories = items[item_name]["calories"]
            
            if cost <= w:
                # Перевіряємо чи краще додати цю страву
                new_value = dp[w - cost] + calories
                if new_value > dp[w]:
                    dp[w] = new_value
                    # Копіюємо попередній вибір
                    choices[w] = choices[w - cost].copy()
                    # Додаємо поточну страву
                    choices[w][item_name] = choices[w].get(item_name, 0) + 1
    
    return choices[budget]


def calculate_totals(
    items: Dict[str, Dict[str, int]],
    selected: Dict[str, int]
) -> Tuple[int, int]:
    """
    Обчислює загальну вартість та калорійність вибраних страв.

    Args:
        items: Словник страв з вартістю та калорійністю.
        selected: Словник вибраних страв та їх кількості.

    Returns:
        Tuple[int, int]: Загальна вартість та калорійність.
    """
    total_cost = 0
    total_calories = 0
    
    for name, quantity in selected.items():
        total_cost += items[name]["cost"] * quantity
        total_calories += items[name]["calories"] * quantity
    
    return total_cost, total_calories


def print_results(
    method_name: str,
    selected: Dict[str, int],
    items: Dict[str, Dict[str, int]],
    budget: int
) -> None:
    """
    Виводить результати вибору страв.

    Args:
        method_name: Назва методу (Жадібний або Динамічне програмування).
        selected: Словник вибраних страв та їх кількості.
        items: Словник страв з вартістю та калорійністю.
        budget: Доступний бюджет.
    """
    print(f"\n{'='*60}")
    print(f"{method_name}")
    print(f"{'='*60}")
    print(f"Бюджет: {budget}")
    print("\nВибрані страви:")
    
    if not selected:
        print("  Немає вибраних страв")
    else:
        for name, quantity in selected.items():
            cost = items[name]["cost"]
            calories = items[name]["calories"]
            print(
                f"  {name}: {quantity} шт. "
                f"(вартість: {cost * quantity}, калорії: {calories * quantity})"
            )
    
    total_cost, total_calories = calculate_totals(items, selected)
    print(f"\nЗагальна вартість: {total_cost}")
    print(f"Загальна калорійність: {total_calories}")
    print(f"Залишок бюджету: {budget - total_cost}")
    print(f"{'='*60}")


def main() -> None:
    """Головна функція програми."""
    print("="*60)
    print("ОПТИМІЗАЦІЯ ВИБОРУ ЇЖІ")
    print("="*60)
    
    # Показуємо доступні страви
    print("\nДоступні страви:")
    for name, info in items.items():
        ratio = info["calories"] / info["cost"]
        print(
            f"  {name}: вартість={info['cost']}, "
            f"калорії={info['calories']}, "
            f"співвідношення={ratio:.2f}"
        )
    
    # Тестуємо з різними бюджетами
    budgets = [50, 100, 150, 200]
    
    for budget in budgets:
        # Жадібний алгоритм
        greedy_result = greedy_algorithm(items, budget)
        print_results("ЖАДІБНИЙ АЛГОРИТМ", greedy_result, items, budget)
        
        # Динамічне програмування
        dp_result = dynamic_programming(items, budget)
        print_results("ДИНАМІЧНЕ ПРОГРАМУВАННЯ", dp_result, items, budget)
        
        # Порівняння результатів
        greedy_cost, greedy_calories = calculate_totals(items, greedy_result)
        dp_cost, dp_calories = calculate_totals(items, dp_result)
        
        print(f"\n{'='*60}")
        print("ПОРІВНЯННЯ")
        print(f"{'='*60}")
        print(
            f"Жадібний алгоритм:       "
            f"калорії={greedy_calories}, вартість={greedy_cost}"
        )
        print(
            f"Динамічне програмування: "
            f"калорії={dp_calories}, вартість={dp_cost}"
        )
        
        if dp_calories > greedy_calories:
            diff = dp_calories - greedy_calories
            if greedy_calories > 0:
                percent = (diff / greedy_calories) * 100
                print(
                    f"\n✓ Динамічне програмування краще на {diff} калорій "
                    f"({percent:.1f}%)"
                )
            else:
                print(f"\n✓ Динамічне програмування краще на {diff} калорій")
        elif greedy_calories > dp_calories:
            diff = greedy_calories - dp_calories
            if dp_calories > 0:
                percent = (diff / dp_calories) * 100
                print(
                    f"\n✓ Жадібний алгоритм краще на {diff} калорій "
                    f"({percent:.1f}%)"
                )
            else:
                print(f"\n✓ Жадібний алгоритм краще на {diff} калорій")
        else:
            print("\n✓ Обидва алгоритми дають однаковий результат")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
