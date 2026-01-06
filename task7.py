"""
Модуль для симуляції кидків кубиків методом Монте-Карло.

Імітує велику кількість кидків двох кубиків, обчислює ймовірності
кожної можливої суми та порівнює результати з теоретичними значеннями.
"""

import random
from typing import Dict, Tuple
import matplotlib.pyplot as plt


# Теоретичні ймовірності (аналітичні розрахунки)
THEORETICAL_PROBABILITIES = {
    2: 1/36,   # 2.78%
    3: 2/36,   # 5.56%
    4: 3/36,   # 8.33%
    5: 4/36,   # 11.11%
    6: 5/36,   # 13.89%
    7: 6/36,   # 16.67%
    8: 5/36,   # 13.89%
    9: 4/36,   # 11.11%
    10: 3/36,  # 8.33%
    11: 2/36,  # 5.56%
    12: 1/36   # 2.78%
}


def roll_dice() -> int:
    """
    Симулює кидок одного кубика.

    Returns:
        int: Випадкове число від 1 до 6.
    """
    return random.randint(1, 6)


def roll_two_dice() -> int:
    """
    Симулює кидок двох кубиків та повертає їх суму.

    Returns:
        int: Сума чисел, що випали на двох кубиках (від 2 до 12).
    """
    return roll_dice() + roll_dice()


def monte_carlo_simulation(num_trials: int) -> Dict[int, float]:
    """
    Виконує симуляцію методом Монте-Карло для кидків двох кубиків.

    Args:
        num_trials: Кількість кидків для симуляції.

    Returns:
        Dict[int, float]: Словник з ймовірностями для кожної суми.
    """
    # Лічильник для кожної можливої суми
    counts: Dict[int, int] = {i: 0 for i in range(2, 13)}
    
    # Виконуємо симуляцію
    for _ in range(num_trials):
        dice_sum = roll_two_dice()
        counts[dice_sum] += 1
    
    # Обчислюємо ймовірності
    probabilities: Dict[int, float] = {}
    for dice_sum, count in counts.items():
        probabilities[dice_sum] = count / num_trials
    
    return probabilities


def calculate_error(
    simulated: Dict[int, float],
    theoretical: Dict[int, float]
) -> Dict[int, float]:
    """
    Обчислює відхилення між симульованими та теоретичними ймовірностями.

    Args:
        simulated: Симульовані ймовірності.
        theoretical: Теоретичні ймовірності.

    Returns:
        Dict[int, float]: Словник з відхиленнями для кожної суми.
    """
    errors: Dict[int, float] = {}
    for dice_sum in simulated:
        errors[dice_sum] = abs(simulated[dice_sum] - theoretical[dice_sum])
    return errors


def print_results_table(
    simulated: Dict[int, float],
    theoretical: Dict[int, float],
    num_trials: int
) -> None:
    """
    Виводить таблицю з результатами симуляції та порівнянням.

    Args:
        simulated: Симульовані ймовірності.
        theoretical: Теоретичні ймовірності.
        num_trials: Кількість проведених випробувань.
    """
    print("=" * 80)
    print(f"РЕЗУЛЬТАТИ СИМУЛЯЦІЇ МЕТОДОМ МОНТЕ-КАРЛО ({num_trials:,} кидків)")
    print("=" * 80)
    print(f"{'Сума':<6} {'Монте-Карло':<15} {'Теоретична':<15} "
          f"{'Відхилення':<15} {'Різниця %':<10}")
    print("-" * 80)
    
    errors = calculate_error(simulated, theoretical)
    
    for dice_sum in sorted(simulated.keys()):
        sim_prob = simulated[dice_sum]
        theo_prob = theoretical[dice_sum]
        error = errors[dice_sum]
        diff_percent = (error / theo_prob) * 100 if theo_prob > 0 else 0
        
        print(
            f"{dice_sum:<6} "
            f"{sim_prob*100:>6.2f}% ({sim_prob:.6f})  "
            f"{theo_prob*100:>6.2f}% ({theo_prob:.6f})  "
            f"{error*100:>6.3f}%          "
            f"{diff_percent:>6.2f}%"
        )
    
    print("-" * 80)
    avg_error = sum(errors.values()) / len(errors) * 100
    print(f"Середнє відхилення: {avg_error:.4f}%")
    print("=" * 80)


def plot_comparison(
    simulated: Dict[int, float],
    theoretical: Dict[int, float],
    num_trials: int
) -> None:
    """
    Створює графік порівняння симульованих та теоретичних ймовірностей.

    Args:
        simulated: Симульовані ймовірності.
        theoretical: Теоретичні ймовірності.
        num_trials: Кількість проведених випробувань.
    """
    sums = sorted(simulated.keys())
    sim_probs = [simulated[s] * 100 for s in sums]
    theo_probs = [theoretical[s] * 100 for s in sums]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Графік 1: Порівняння ймовірностей
    x = range(len(sums))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], sim_probs, width, 
            label='Монте-Карло', alpha=0.8, color='steelblue')
    ax1.bar([i + width/2 for i in x], theo_probs, width,
            label='Теоретичні', alpha=0.8, color='coral')
    
    ax1.set_xlabel('Сума на кубиках', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Ймовірність (%)', fontsize=12, fontweight='bold')
    ax1.set_title(
        f'Порівняння ймовірностей (симуляція: {num_trials:,} кидків)',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(sums)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Додаємо значення на стовпчиках
    for i, (sim, theo) in enumerate(zip(sim_probs, theo_probs)):
        ax1.text(i - width/2, sim + 0.3, f'{sim:.2f}%', 
                ha='center', va='bottom', fontsize=9)
        ax1.text(i + width/2, theo + 0.3, f'{theo:.2f}%',
                ha='center', va='bottom', fontsize=9)
    
    # Графік 2: Відхилення
    errors = calculate_error(simulated, theoretical)
    error_probs = [errors[s] * 100 for s in sums]
    
    ax2.bar(x, error_probs, color='crimson', alpha=0.7)
    ax2.set_xlabel('Сума на кубиках', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Абсолютне відхилення (%)', fontsize=12, fontweight='bold')
    ax2.set_title(
        'Відхилення від теоретичних значень',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(sums)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Додаємо значення на стовпчиках
    for i, err in enumerate(error_probs):
        ax2.text(i, err + 0.02, f'{err:.3f}%',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.show()


def run_multiple_simulations(
    trial_sizes: Tuple[int, ...]
) -> None:
    """
    Виконує кілька симуляцій з різною кількістю кидків.

    Args:
        trial_sizes: Кортеж з кількостями кидків для кожної симуляції.
    """
    print("\n" + "=" * 80)
    print("ПОРІВНЯННЯ СИМУЛЯЦІЙ З РІЗНОЮ КІЛЬКІСТЮ КИДКІВ")
    print("=" * 80 + "\n")
    
    for num_trials in trial_sizes:
        simulated = monte_carlo_simulation(num_trials)
        print_results_table(simulated, THEORETICAL_PROBABILITIES, num_trials)
        print()


def main() -> None:
    """Головна функція програми."""
    print("\n" + "=" * 80)
    print("СИМУЛЯЦІЯ КИДКІВ КУБИКІВ МЕТОДОМ МОНТЕ-КАРЛО")
    print("=" * 80)
    
    # Показуємо теоретичні ймовірності
    print("\nТеоретичні ймовірності (аналітичні розрахунки):")
    print("-" * 80)
    print(f"{'Сума':<10} {'Комбінацій':<15} {'Ймовірність':<20} {'Відсоток':<10}")
    print("-" * 80)
    
    combinations = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
                   8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    
    for dice_sum in sorted(THEORETICAL_PROBABILITIES.keys()):
        prob = THEORETICAL_PROBABILITIES[dice_sum]
        comb = combinations[dice_sum]
        print(
            f"{dice_sum:<10} {comb}/36 ({comb:<2})      "
            f"{prob:.6f}           {prob*100:.2f}%"
        )
    print("-" * 80)
    
    # Виконуємо симуляції з різною кількістю кидків
    trial_sizes = (1_000, 10_000, 100_000, 1_000_000)
    run_multiple_simulations(trial_sizes)
    
    # Виконуємо детальну симуляцію з великою кількістю кидків
    print("\n" + "=" * 80)
    print("ДЕТАЛЬНА СИМУЛЯЦІЯ З ВІЗУАЛІЗАЦІЄЮ")
    print("=" * 80 + "\n")
    
    num_trials = 1_000_000
    print(f"Виконання симуляції з {num_trials:,} кидків...")
    simulated = monte_carlo_simulation(num_trials)
    
    print_results_table(simulated, THEORETICAL_PROBABILITIES, num_trials)
    
    # Створюємо графік
    print("\nСтворення графіка порівняння...")
    plot_comparison(simulated, THEORETICAL_PROBABILITIES, num_trials)
    
    print("\n" + "=" * 80)
    print("ВИСНОВКИ")
    print("=" * 80)
    print("""
Метод Монте-Карло дозволяє отримати ймовірності, дуже близькі до
теоретичних значень. Точність результатів зростає зі збільшенням
кількості випробувань:

- При 1,000 кидків: помітні відхилення (0.1-1%)
- При 10,000 кидків: відхилення зменшуються (0.05-0.5%)
- При 100,000 кидків: відхилення мінімальні (0.01-0.1%)
- При 1,000,000 кидків: результати майже збігаються з теоретичними

Це підтверджує закон великих чисел: при збільшенні кількості
експериментів емпіричні ймовірності наближаються до теоретичних.
    """)
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Встановлюємо seed для відтворюваності результатів (опціонально)
    # random.seed(42)
    main()
