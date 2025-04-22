import tkinter as tk
from tkinter import simpledialog, messagebox
from binary_tree import BinaryTree, TreeNode


class BinaryTreeApp:
    def __init__(self, root):
        self.root = root
        self.tree = None
        self.canvas = None
        self.node_radius = 20
        self.horizontal_spacing = 40
        self.vertical_spacing = 80
        self._after_id = None

        self._setup_ui()
        self.generate_random_tree()
        self.root.bind("<Configure>", self._safe_redraw)

    #Настройка интерфейса
    def _setup_ui(self):
        self.root.title("Визуализация бинарного дерева")

        # Панель управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Случайное дерево", command=self.generate_random_tree).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="T: Вставить", command=self.run_insert).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="D: Удалить", command=self.run_delete).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Очистить", command=self.clear_tree).pack(side=tk.LEFT, padx=5)

        # Холст для рисования
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    # Безопасная перерисовка с задержкой
    def _safe_redraw(self, event=None):
        if hasattr(self, 'tree') and self.tree:
            if self._after_id:
                self.root.after_cancel(self._after_id)
            self._after_id = self.root.after(100, self._draw_tree)

    # Генерация случайного дерева
    def generate_random_tree(self):
        self.tree = BinaryTree.generate_random_tree()
        self._draw_tree()


    # Очистка холста
    def clear_tree(self):
        self.tree = None
        self.canvas.delete("all")

    # Выполнение вставки
    def run_insert(self):
        if not self.tree:
            self.tree = TreeNode(50)

        value = self._ask_value("Введите значение для вставки")
        if value is not None:
            self.tree = BinaryTree.insert(self.tree, value)
            self._draw_tree()

    # Выполнение удаления
    def run_delete(self):
        if not self.tree:
            messagebox.showwarning("Ошибка", "Дерево пустое!")
            return

        value = self._ask_value("Введите значение для удаления")
        if value is not None:
            if not BinaryTree.search(self.tree, value):
                messagebox.showwarning("Ошибка", "Значение не найдено!")
            else:
                self.tree = BinaryTree.delete(self.tree, value)
                self._draw_tree()

    # Диалог ввода значения
    def _ask_value(self, title):
        try:
            return int(simpledialog.askstring(title, "Введите число:"))
        except (TypeError, ValueError):
            return None

    # Отрисовка дерева с автоматическим масштабированием
    def _draw_tree(self):
        self.canvas.delete("all")
        if not self.tree:
            return

        # Получаем актуальные размеры холста
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0:
            return

        # Вычисляем глубину дерева
        depth = BinaryTree.get_tree_depth(self.tree)
        if depth <= 0:
            return

        # Автоматический расчет параметров отрисовки
        max_levels = min(depth, 5)  # Ограничиваем глубину отрисовки
        self.vertical_spacing = (canvas_height - 100) // (max_levels + 1)

        # Рассчитываем горизонтальные расстояния
        max_nodes = 2 ** (max_levels - 1)
        required_width = max_nodes * (self.node_radius * 2 + 20)
        self.horizontal_spacing = min(60, (canvas_width - 100) // max_nodes)

        # Стартовая позиция (по центру)
        start_x = canvas_width // 2
        start_y = 50 + self.node_radius

        # Рекурсивная отрисовка
        self._draw_node(self.tree, start_x, start_y,
                        self.horizontal_spacing * (2 ** (max_levels - 1)),
                        max_levels, 1)

    # Рекурсивная отрисовка узлов
    def _draw_node(self, node, x, y, spacing, max_depth, current_depth):
        if not node or current_depth > max_depth:
            return

        # Получаем размеры холста
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Проверяем видимость узла
        if (x - self.node_radius < 0 or x + self.node_radius > canvas_width or
                y - self.node_radius < 0 or y + self.node_radius > canvas_height):
            return

        # Отрисовываем связи с потомками
        if node.left and current_depth < max_depth:
            left_x = x - spacing / 2
            left_y = y + self.vertical_spacing
            if (0 <= left_x <= canvas_width and 0 <= left_y <= canvas_height):
                self.canvas.create_line(x, y + self.node_radius, left_x, left_y - self.node_radius, fill='black')
                self._draw_node(node.left, left_x, left_y, spacing / 2, max_depth, current_depth + 1)

        if node.right and current_depth < max_depth:
            right_x = x + spacing / 2
            right_y = y + self.vertical_spacing
            if (0 <= right_x <= canvas_width and 0 <= right_y <= canvas_height):
                self.canvas.create_line(x, y + self.node_radius, right_x, right_y - self.node_radius, fill='black')
                self._draw_node(node.right, right_x, right_y, spacing / 2, max_depth, current_depth + 1)

        # Отрисовываем узел
        self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill='lightblue', outline='black'
        )
        self.canvas.create_text(x, y, text=str(node.value), font=('Arial', 10, 'bold'))


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root)
    root.mainloop()