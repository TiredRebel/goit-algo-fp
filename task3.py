"""
Модуль для реалізації алгоритму Дейкстри з використанням бінарної купи.

Цей модуль містить класи та функції для знаходження найкоротших шляхів
у зваженому графі за допомогою алгоритму Дейкстри з оптимізацією
через бінарну купу (піраміду).
"""

import heapq
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field


@dataclass
class Edge:
    """
    Клас для представлення ребра графа.

    Attributes:
        destination: Вершина призначення
        weight: Вага ребра
    """
    destination: int
    weight: float

    def __post_init__(self) -> None:
        """Перевірка валідності ваги ребра."""
        if self.weight < 0:
            raise ValueError("Вага ребра не може бути від'ємною")


@dataclass
class Graph:
    """
    Клас для представлення зваженого графа.

    Attributes:
        vertices: Кількість вершин у графі
        adjacency_list: Список суміжності для представлення графа
    """
    vertices: int
    adjacency_list: Dict[int, List[Edge]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Ініціалізація списку суміжності."""
        if self.vertices <= 0:
            raise ValueError("Кількість вершин повинна бути додатною")

        for i in range(self.vertices):
            if i not in self.adjacency_list:
                self.adjacency_list[i] = []

    def add_edge(self, source: int, destination: int, weight: float) -> None:
        """
        Додає ребро до графа.

        Args:
            source: Початкова вершина
            destination: Кінцева вершина
            weight: Вага ребра

        Raises:
            ValueError: Якщо вершини виходять за межі графа або вага від'ємна
        """
        if not (0 <= source < self.vertices and
                0 <= destination < self.vertices):
            raise ValueError(
                f"Вершини повинні бути в діапазоні [0, {self.vertices - 1}]"
            )

        edge = Edge(destination, weight)
        self.adjacency_list[source].append(edge)

    def add_bidirectional_edge(
        self,
        vertex1: int,
        vertex2: int,
        weight: float
    ) -> None:
        """
        Додає двонаправлене ребро до графа.

        Args:
            vertex1: Перша вершина
            vertex2: Друга вершина
            weight: Вага ребра
        """
        self.add_edge(vertex1, vertex2, weight)
        self.add_edge(vertex2, vertex1, weight)

    def get_neighbors(self, vertex: int) -> List[Edge]:
        """
        Повертає список сусідніх вершин для заданої вершини.

        Args:
            vertex: Вершина, для якої потрібно знайти сусідів

        Returns:
            Список ребер, що виходять з вершини
        """
        if vertex not in self.adjacency_list:
            return []
        return self.adjacency_list[vertex]


@dataclass
class DijkstraResult:
    """
    Клас для зберігання результатів алгоритму Дейкстри.

    Attributes:
        distances: Словник відстаней від початкової вершини до всіх інших
        predecessors: Словник попередників для відновлення шляхів
        source: Початкова вершина
    """
    distances: Dict[int, float]
    predecessors: Dict[int, Optional[int]]
    source: int

    def get_path(self, destination: int) -> Optional[List[int]]:
        """
        Відновлює шлях від початкової вершини до заданої.

        Args:
            destination: Кінцева вершина

        Returns:
            Список вершин, що утворюють шлях, або None якщо шлях не існує
        """
        if destination not in self.distances:
            return None

        if self.distances[destination] == float('inf'):
            return None

        path = []
        current: Optional[int] = destination

        while current is not None:
            path.append(current)
            current = self.predecessors.get(current)

        path.reverse()
        return path

    def get_distance(self, destination: int) -> float:
        """
        Повертає найкоротшу відстань до заданої вершини.

        Args:
            destination: Кінцева вершина

        Returns:
            Відстань до вершини або float('inf') якщо вершина недосяжна
        """
        return self.distances.get(destination, float('inf'))


class DijkstraAlgorithm:
    """
    Клас для реалізації алгоритму Дейкстри з використанням бінарної купи.
    """

    @staticmethod
    def find_shortest_paths(graph: Graph, source: int) -> DijkstraResult:
        """
        Знаходить найкоротші шляхи від початкової вершини до всіх інших
        використовуючи алгоритм Дейкстри з бінарною купою.

        Args:
            graph: Граф, у якому шукаються найкоротші шляхи
            source: Початкова вершина

        Returns:
            Об'єкт DijkstraResult з результатами обчислень

        Raises:
            ValueError: Якщо початкова вершина виходить за межі графа
        """
        if not (0 <= source < graph.vertices):
            raise ValueError(
                f"Початкова вершина повинна бути в діапазоні "
                f"[0, {graph.vertices - 1}]"
            )

        # Ініціалізація відстаней та попередників
        distances: Dict[int, float] = {
            i: float('inf') for i in range(graph.vertices)
        }
        predecessors: Dict[int, Optional[int]] = {
            i: None for i in range(graph.vertices)
        }
        distances[source] = 0

        # Бінарна купа для зберігання вершин (відстань, вершина)
        min_heap: List[Tuple[float, int]] = [(0, source)]

        # Множина відвіданих вершин
        visited: Set[int] = set()

        while min_heap:
            # Вибираємо вершину з найменшою відстанню
            current_distance, current_vertex = heapq.heappop(min_heap)

            # Якщо вершина вже відвідана, пропускаємо
            if current_vertex in visited:
                continue

            # Позначаємо вершину як відвідану
            visited.add(current_vertex)

            # Якщо поточна відстань більша за збережену, пропускаємо
            if current_distance > distances[current_vertex]:
                continue

            # Переглядаємо всіх сусідів поточної вершини
            for edge in graph.get_neighbors(current_vertex):
                neighbor = edge.destination
                weight = edge.weight

                # Пропускаємо вже відвідані вершини
                if neighbor in visited:
                    continue

                # Обчислюємо нову відстань через поточну вершину
                new_distance = distances[current_vertex] + weight

                # Якщо знайдено коротший шлях, оновлюємо відстань
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(min_heap, (new_distance, neighbor))

        return DijkstraResult(
            distances=distances,
            predecessors=predecessors,
            source=source
        )


def print_results(result: DijkstraResult, graph: Graph) -> None:
    """
    Виводить результати роботи алгоритму Дейкстри.

    Args:
        result: Результати обчислень алгоритму Дейкстри
        graph: Граф, для якого виконувались обчислення
    """
    print(f"\nНайкоротші шляхи від вершини {result.source}:")
    print("-" * 60)

    for vertex in range(graph.vertices):
        distance = result.get_distance(vertex)

        if distance == float('inf'):
            print(f"Вершина {vertex}: недосяжна")
        else:
            path = result.get_path(vertex)
            path_str = " -> ".join(map(str, path)) if path else "N/A"
            print(f"Вершина {vertex}: відстань = {distance:.2f}, "
                  f"шлях = {path_str}")


def main() -> None:
    """
    Головна функція для демонстрації роботи алгоритму Дейкстри.
    """
    print("=" * 60)
    print("Демонстрація алгоритму Дейкстри з бінарною купою")
    print("=" * 60)

    # Створення графа
    num_vertices = 6
    graph = Graph(vertices=num_vertices)

    # Додавання ребер до графа
    # Граф представляє транспортну мережу з вагами як відстанями
    edges = [
        (0, 1, 4.0),
        (0, 2, 2.0),
        (1, 2, 1.0),
        (1, 3, 5.0),
        (2, 3, 8.0),
        (2, 4, 10.0),
        (3, 4, 2.0),
        (3, 5, 6.0),
        (4, 5, 3.0)
    ]

    print(f"\nСтворюємо граф з {num_vertices} вершинами")
    print("\nДодаємо ребра:")
    for source, dest, weight in edges:
        graph.add_edge(source, dest, weight)
        print(f"  {source} -> {dest} (вага: {weight})")

    # Виконання алгоритму Дейкстри
    start_vertex = 0
    print(f"\n\nВиконуємо алгоритм Дейкстри від вершини {start_vertex}...")

    dijkstra = DijkstraAlgorithm()
    result = dijkstra.find_shortest_paths(graph, start_vertex)

    # Виведення результатів
    print_results(result, graph)

    # Приклад двонаправленого графа
    print("\n\n" + "=" * 60)
    print("Приклад з двонаправленим графом")
    print("=" * 60)

    graph2 = Graph(vertices=5)
    bidirectional_edges = [
        (0, 1, 10.0),
        (0, 4, 5.0),
        (1, 2, 1.0),
        (1, 4, 2.0),
        (2, 3, 4.0),
        (3, 0, 7.0),
        (3, 2, 6.0),
        (4, 1, 3.0),
        (4, 2, 9.0),
        (4, 3, 2.0)
    ]

    print(f"\nСтворюємо двонаправлений граф з {graph2.vertices} вершинами")
    print("\nДодаємо двонаправлені ребра:")
    for v1, v2, weight in bidirectional_edges:
        graph2.add_bidirectional_edge(v1, v2, weight)
        print(f"  {v1} <-> {v2} (вага: {weight})")

    start_vertex2 = 0
    result2 = dijkstra.find_shortest_paths(graph2, start_vertex2)
    print_results(result2, graph2)

    print("\n" + "=" * 60)
    print("Демонстрація завершена")
    print("=" * 60)


if __name__ == "__main__":
    main()