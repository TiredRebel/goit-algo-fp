"""
Модуль для візуалізації обходу бінарного дерева.

Реалізує візуалізацію обходів дерева в глибину (DFS) та в ширину (BFS)
з використанням різних кольорів для відображення послідовності відвідування вузлів.
"""

import uuid
from typing import Optional, Dict, Tuple, List, cast
from collections import deque
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
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.val: int = key
        self.color: str = color
        self.id: str = str(uuid.uuid4())


def generate_color_gradient(steps: int) -> List[str]:
    """
    Генерує градієнт кольорів від темного до світлого.

    Args:
        steps: Кількість кольорів у градієнті.

    Returns:
        List[str]: Список кольорів у форматі HEX.
    """
    colors = []
    for i in range(steps):
        # Від темного (#1B1464) до світлого (#E8F4FF)
        # Інтерполяція від темно-синього до світло-блакитного
        ratio = i / max(steps - 1, 1)
        
        # Початковий колір (темний)
        r_start, g_start, b_start = 27, 20, 100
        # Кінцевий колір (світлий)
        r_end, g_end, b_end = 232, 244, 255
        
        r = int(r_start + (r_end - r_start) * ratio)
        g = int(g_start + (g_end - g_start) * ratio)
        b = int(b_start + (b_end - b_start) * ratio)
        
        color = f"#{r:02X}{g:02X}{b:02X}"
        colors.append(color)
    
    return colors


def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: Dict[str, Tuple[float, float]],
    x: float = 0.0,
    y: float = 0.0,
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
        nx.DiGraph: Оновлений граф.
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


def draw_tree(
    tree_root: Node,
    title: str = "Бінарне дерево",
    node_colors: Optional[Dict[str, str]] = None
) -> None:
    """
    Візуалізує бінарне дерево.

    Args:
        tree_root: Корінь дерева.
        title: Заголовок візуалізації.
        node_colors: Словник кольорів для вузлів {node_id: color}.
    """
    tree = nx.DiGraph()
    pos: Dict[str, Tuple[float, float]] = {tree_root.id: (0.0, 0.0)}
    tree = add_edges(tree, tree_root, pos)

    # Якщо передано кастомні кольори, використовуємо їх
    if node_colors:
        colors = cast(
            List[str],
            [
                node_colors.get(node[0], node[1].get('color', 'skyblue'))
                for node in tree.nodes(data=True)
            ]
        )
    else:
        colors = cast(
            List[str],
            [node[1].get('color', 'skyblue') for node in tree.nodes(data=True)]
        )
    
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        node_size=2500,
        node_color=colors,
        font_size=16,
        font_weight='bold'
    )
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.show()


def dfs_traversal(root: Optional[Node]) -> List[Node]:
    """
    Обхід дерева в глибину (DFS) з використанням стека.

    Args:
        root: Корінь дерева або None.

    Returns:
        List[Node]: Список вузлів у порядку обходу.
    """
    if not root:
        return []
    
    stack: List[Node] = [root]
    visited: List[Node] = []
    
    while stack:
        node = stack.pop()
        visited.append(node)
        
        # Додаємо дітей у зворотному порядку (спочатку праву, потім ліву)
        # щоб ліва оброблялася першою при pop()
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return visited


def bfs_traversal(root: Optional[Node]) -> List[Node]:
    """
    Обхід дерева в ширину (BFS) з використанням черги.

    Args:
        root: Корінь дерева або None.

    Returns:
        List[Node]: Список вузлів у порядку обходу.
    """
    if not root:
        return []
    
    queue: deque[Node] = deque([root])
    visited: List[Node] = []
    
    while queue:
        node = queue.popleft()
        visited.append(node)
        
        # Додаємо дітей зліва направо
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return visited


def visualize_traversal(
    root: Node,
    traversal_type: str = "DFS"
) -> None:
    """
    Візуалізує обхід дерева з градієнтом кольорів.

    Args:
        root: Корінь дерева.
        traversal_type: Тип обходу ("DFS" або "BFS").
    """
    # Виконуємо обхід
    if traversal_type.upper() == "DFS":
        visited_nodes = dfs_traversal(root)
        title = "Обхід дерева в глибину (DFS)"
    elif traversal_type.upper() == "BFS":
        visited_nodes = bfs_traversal(root)
        title = "Обхід дерева в ширину (BFS)"
    else:
        raise ValueError("traversal_type має бути 'DFS' або 'BFS'")
    
    # Генеруємо градієнт кольорів
    colors = generate_color_gradient(len(visited_nodes))
    
    # Створюємо словник кольорів для вузлів
    node_colors: Dict[str, str] = {}
    for i, node in enumerate(visited_nodes):
        node_colors[node.id] = colors[i]
    
    # Виводимо порядок обходу
    print(f"\n{title}:")
    print("Порядок відвідування вузлів:")
    for i, node in enumerate(visited_nodes, 1):
        print(f"  {i}. Вузол {node.val} (колір: {colors[i-1]})")
    
    # Візуалізуємо дерево з кольорами
    draw_tree(root, title, node_colors)


def create_sample_tree() -> Node:
    """
    Створює приклад бінарного дерева для демонстрації.

    Returns:
        Node: Корінь створеного дерева.
    """
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root


def create_larger_tree() -> Node:
    """
    Створює більше бінарне дерево для демонстрації.

    Returns:
        Node: Корінь створеного дерева.
    """
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    root.left.left.left = Node(8)
    root.left.left.right = Node(9)
    return root


def main() -> None:
    """Головна функція програми."""
    print("=" * 60)
    print("ВІЗУАЛІЗАЦІЯ ОБХОДУ БІНАРНОГО ДЕРЕВА")
    print("=" * 60)
    
    # Приклад 1: Маленьке дерево з завдання
    print("\nПриклад 1: Дерево з завдання")
    tree1 = create_sample_tree()
    
    # DFS обхід
    visualize_traversal(tree1, "DFS")
    
    # BFS обхід
    visualize_traversal(tree1, "BFS")
    
    # Приклад 2: Більше дерево
    print("\nПриклад 2: Більше дерево")
    tree2 = create_larger_tree()
    
    # DFS обхід
    visualize_traversal(tree2, "DFS")
    
    # BFS обхід
    visualize_traversal(tree2, "BFS")
    
    print("\n" + "=" * 60)
    print("Візуалізація завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
