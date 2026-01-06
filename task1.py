"""
Модуль для роботи з однозв'язним списком.

Реалізує структуру даних однозв'язний список та операції над ним:
- реверсування списку
- сортування злиттям
- об'єднання двох відсортованих списків
"""

from typing import Optional


class Node:
    """Клас вузла однозв'язного списку."""

    def __init__(self, data: int) -> None:
        """
        Ініціалізація вузла.

        Args:
            data: Дані вузла
        """
        self.data = data
        self.next: Optional['Node'] = None


class LinkedList:
    """Клас однозв'язного списку."""

    def __init__(self) -> None:
        """Ініціалізація порожнього списку."""
        self.head: Optional[Node] = None

    def insert_at_beginning(self, data: int) -> None:
        """
        Вставляє новий вузол на початок списку.

        Args:
            data: Дані для нового вузла
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data: int) -> None:
        """
        Вставляє новий вузол в кінець списку.

        Args:
            data: Дані для нового вузла
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self) -> None:
        """Виводить елементи списку."""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) if elements else "Список порожній")

    def to_list(self) -> list[int]:
        """
        Конвертує однозв'язний список у Python list.

        Returns:
            list[int]: Список елементів
        """
        result: list[int] = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


def reverse_linked_list(linked_list: LinkedList) -> LinkedList:
    """
    Реверсує однозв'язний список, змінюючи посилання між вузлами.

    Args:
        linked_list: Вхідний однозв'язний список

    Returns:
        LinkedList: Реверсований список
    """
    prev = None
    current = linked_list.head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    linked_list.head = prev
    return linked_list


def merge_sorted_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """
    Об'єднує два відсортовані однозв'язні списки в один відсортований.

    Args:
        list1: Перший відсортований список
        list2: Другий відсортований список

    Returns:
        LinkedList: Об'єднаний відсортований список
    """
    dummy = Node(0)
    tail = dummy

    node1 = list1.head
    node2 = list2.head

    while node1 and node2:
        if node1.data <= node2.data:
            tail.next = node1
            node1 = node1.next
        else:
            tail.next = node2
            node2 = node2.next
        tail = tail.next

    tail.next = node1 if node1 else node2

    merged_list = LinkedList()
    merged_list.head = dummy.next
    return merged_list


def merge_sort_linked_list(linked_list: LinkedList) -> LinkedList:
    """
    Сортує однозв'язний список методом злиття.

    Args:
        linked_list: Вхідний список

    Returns:
        LinkedList: Відсортований список
    """
    head = linked_list.head
    if head is None or head.next is None:
        return linked_list  # Вже відсортований

    # Рекурсивна функція для сортування, що працює з вузлами
    def sort(node: Optional[Node]) -> Optional[Node]:
        if node is None or node.next is None:
            return node

        # Розділення списку на дві половини
        middle = get_middle(node)
        if middle is None:
            return node
        
        next_to_middle = middle.next
        middle.next = None

        # Рекурсивне сортування
        left_half = sort(node)
        right_half = sort(next_to_middle)

        # Злиття відсортованих половин
        sorted_node = merge_sorted_lists_nodes(left_half, right_half)
        return sorted_node

    linked_list.head = sort(head)
    return linked_list


def get_middle(head: Optional[Node]) -> Optional[Node]:
    """
    Знаходить середній вузол списку методом двох вказівників.

    Args:
        head: Голова списку

    Returns:
        Optional[Node]: Середній вузол або None якщо список порожній
    """
    if head is None:
        return None

    slow: Optional[Node] = head
    fast: Optional[Node] = head

    while fast and fast.next and fast.next.next:
        if slow:
            slow = slow.next
        fast = fast.next.next

    return slow


def merge_sorted_lists_nodes(node1: Optional[Node], node2: Optional[Node]) -> Optional[Node]:
    """
    Допоміжна функція для об'єднання двох відсортованих списків (представлених вузлами).

    Args:
        node1: Голова першого відсортованого списку
        node2: Голова другого відсортованого списку

    Returns:
        Optional[Node]: Голова об'єднаного відсортованого списку
    """
    dummy = Node(0)
    tail = dummy

    while node1 and node2:
        if node1.data <= node2.data:
            tail.next = node1
            node1 = node1.next
        else:
            tail.next = node2
            node2 = node2.next
        tail = tail.next

    tail.next = node1 if node1 else node2

    return dummy.next


def main() -> None:
    """Точка входу в програму."""
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ РОБОТИ З ОДНОЗВ'ЯЗНИМ СПИСКОМ")
    print("=" * 60)

    # Створення першого списку
    print("\n1. Створення та виведення списку:")
    llist = LinkedList()
    llist.insert_at_end(5)
    llist.insert_at_end(3)
    llist.insert_at_end(8)
    llist.insert_at_end(1)
    llist.insert_at_end(9)
    print("Початковий список:")
    llist.print_list()

    # Реверсування списку
    print("\n2. Реверсування списку:")
    llist = reverse_linked_list(llist)
    print("Реверсований список:")
    llist.print_list()

    # Сортування списку
    print("\n3. Сортування списку методом злиття:")
    llist = merge_sort_linked_list(llist)
    print("Відсортований список:")
    llist.print_list()

    # Об'єднання двох відсортованих списків
    print("\n4. Об'єднання двох відсортованих списків:")
    list1 = LinkedList()
    list1.insert_at_end(1)
    list1.insert_at_end(3)
    list1.insert_at_end(5)
    print("Перший список:")
    list1.print_list()

    list2 = LinkedList()
    list2.insert_at_end(2)
    list2.insert_at_end(4)
    list2.insert_at_end(6)
    print("Другий список:")
    list2.print_list()

    merged = merge_sorted_lists(list1, list2)
    print("Об'єднаний відсортований список:")
    merged.print_list()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()