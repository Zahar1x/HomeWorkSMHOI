import random

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:

    # Создаем сбалансированное бинарное дерево из отсортированного списка.
    def create_balanced_tree(values):
        if not values:
            return None
        values.sort()

        def _build_balanced(start, end):
            if start > end:
                return None
            mid = (start + end) // 2
            node = TreeNode(values[mid])
            node.left = _build_balanced(start, mid - 1)
            node.right = _build_balanced(mid + 1, end)
            return node

        return _build_balanced(0, len(values) - 1)

    # Генерируем случайный сбалансированный список.
    def generate_random_tree(min_nodes=7, max_nodes=15, min_val=1, max_val=100):
        num_nodes = random.randint(min_nodes, max_nodes)
        values = random.sample(range(min_val, max_val), num_nodes)
        return BinaryTree.create_balanced_tree(values)


    # Возвращает глубину дерева.
    def get_tree_depth(node):
        if not node:
            return 0
        left_depth = BinaryTree.get_tree_depth(node.left)
        right_depth = BinaryTree.get_tree_depth(node.right)
        return max(left_depth, right_depth) + 1


    # Рекурсивный поиск узла по значению.
    def search(node, value):
        if not node:
            return None
        if value == node.value:
            return node
        elif value < node.value:
            return BinaryTree.search(node.left, value)
        else:
            return BinaryTree.search(node.right, value)

    # T-алгоритм: поиск со вставкой (если элемента нет)
    def insert(root, value):
        if not root:
            return TreeNode(value)
        if value < root.value:
            root.left = BinaryTree.insert(root.left, value)
        elif value > root.value:
            root.right = BinaryTree.insert(root.right, value)
        return root  # Если значение уже есть, ничего не меняем

    # D-алгоритм: удаление узла по значению.
    def delete(root, value):
        if not root:
            return None

        # Поиск узла
        if value < root.value:
            root.left = BinaryTree.delete(root.left, value)
        elif value > root.value:
            root.right = BinaryTree.delete(root.right, value)
        else:  # Узел найден
            # Случай 1: Нет потомков или только один
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            # Случай 2: Два потомка -> находим минимальный в правом поддереве
            min_node = BinaryTree._find_min(root.right)
            root.value = min_node.value
            root.right = BinaryTree.delete(root.right, min_node.value)
        return root


    # Возвращает узел с минимальным значением в поддереве.
    def _find_min(node):
        while node.left:
            node = node.left
        return node