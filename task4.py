"""Модуль для візуалізації бінарної купи."""

import uuid
from typing import Optional, Dict, Tuple, List
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """Клас для представлення вузла бінарного дерева."""

    def __init__(self, key: int, color: str = "skyblue") -> None:
        """
        Ініціалізація вузла дерева.

        Args:
            key: Значення вузла.
            color: Колір вузла для візуалізації.
        """
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.val: int = key
        self.color: str = color
        self.id: str = str(uuid.uuid4())


def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: Dict[str, Tuple[float, float]],
    x: float = 0,
    y: float = 0,
    layer: int = 1
) -> nx.DiGraph:
    """
    Рекурсивно додає ребра та вузли до графа.

    Args:
        graph: Орієнтований граф NetworkX.
        node: Поточний вузол дерева.
        pos: Словник позицій вузлів.
        x: Координата X поточного вузла.
        y: Координата Y поточного вузла.
        layer: Рівень глибини в дереві.

    Returns:
        Оновлений граф.
    """
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2 ** layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2 ** layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root: Node, title: str = "Бінарне дерево") -> None:
    """
    Візуалізує бінарне дерево.

    Args:
        tree_root: Корінь дерева.
        title: Заголовок візуалізації.
    """
    tree = nx.DiGraph()
    pos: Dict[str, Tuple[float, float]] = {tree_root.id: (0.0, 0.0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        node_size=2500,
        node_color=colors
    )
    plt.title(title)
    plt.show()


def heap_to_tree(heap: List[int], index: int = 0) -> Optional[Node]:
    """
    Перетворює масив купи у бінарне дерево.

    Args:
        heap: Список елементів купи.
        index: Поточний індекс у масиві купи.

    Returns:
        Корінь побудованого дерева або None.
    """
    if index >= len(heap):
        return None

    node = Node(heap[index])
    left_child_index = 2 * index + 1
    right_child_index = 2 * index + 2

    node.left = heap_to_tree(heap, left_child_index)
    node.right = heap_to_tree(heap, right_child_index)

    return node


def visualize_heap(heap: List[int]) -> None:
    """
    Візуалізує бінарну купу.

    Args:
        heap: Список елементів купи у вигляді масиву.
    """
    if not heap:
        print("Купа порожня!")
        return

    tree_root = heap_to_tree(heap)
    if tree_root:
        draw_tree(tree_root, "Візуалізація бінарної купи")


def main() -> None:
    """Головна функція програми."""
    # Приклад 1: Візуалізація дерева з завдання
    print("Приклад 1: Візуалізація дерева з завдання")
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    draw_tree(root, "Дерево з завдання")

    # Приклад 2: Візуалізація max-купи
    print("\nПриклад 2: Візуалізація max-купи")
    max_heap = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    visualize_heap(max_heap)

    # Приклад 3: Візуалізація min-купи
    print("\nПриклад 3: Візуалізація min-купи")
    min_heap = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    visualize_heap(min_heap)

    # Приклад 4: Купа з завдання (відповідає зображенню)
    print("\nПриклад 4: Купа з завдання")
    task_heap = [0, 4, 1, 5, 10, 3]
    visualize_heap(task_heap)


if __name__ == "__main__":
    main()