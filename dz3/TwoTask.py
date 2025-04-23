import tkinter as tk
from tkinter import simpledialog, messagebox
from binary_tree import BinaryTree, TreeNode


class BinaryTreeVisualizer:
    """Класс для визуализации бинарного дерева с использованием Tkinter."""

    def __init__(self, master):
        """
        Инициализация приложения.

        Args:
            master: Главное окно Tkinter
        """
        self.master = master
        self.tree = None
        self.canvas = None

        # Конфигурация отрисовки
        self.node_radius = 20
        self.horizontal_spacing = 40
        self.vertical_spacing = 80
        self.max_display_depth = 5  # Инициализация отсутствующего атрибута

        self._setup_ui()
        self.generate_random_tree()

        # Оптимизация перерисовки
        self._redraw_scheduled = False
        self.master.bind("<Configure>", self.schedule_redraw)

    def _setup_ui(self):
        """Настройка пользовательского интерфейса."""
        self.master.title("Визуализатор бинарного дерева")
        self.master.geometry("800x600")

        self._create_control_panel()
        self._create_canvas()

    def _create_control_panel(self):
        """Создает панель управления."""
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=10, fill=tk.X)

        buttons = [
            ("Случайное дерево", self.generate_random_tree),
            ("Вставить", self.run_insert),
            ("Удалить", self.run_delete),
            ("Очистить", self.clear_tree),
            ("Поиск", self.run_search)
        ]

        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=5, expand=True)

    def _create_canvas(self):
        """Создает холст для отрисовки дерева."""
        self.canvas = tk.Canvas(
            self.master,
            width=800,
            height=550,
            bg='white',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def schedule_redraw(self, event=None):
        """Планирует перерисовку дерева с задержкой."""
        if not self._redraw_scheduled and self.tree:
            self._redraw_scheduled = True
            self.master.after(100, self._execute_redraw)

    def _execute_redraw(self):
        """Выполняет отложенную перерисовку."""
        self._redraw_scheduled = False
        self.draw_tree()

    def generate_random_tree(self):
        """Генерирует случайное дерево и перерисовывает его."""
        self.tree = BinaryTree.generate_random_tree()
        self.draw_tree()

    def clear_tree(self):
        """Очищает дерево и холст."""
        self.tree = None
        self.canvas.delete("all")

    def run_insert(self):
        """Запрашивает значение и вставляет его в дерево."""
        value = self._get_user_input("Введите значение для вставки")
        if value is not None:
            if not self.tree:
                self.tree = TreeNode(value)
            else:
                self.tree = BinaryTree.insert(self.tree, value)
            self.draw_tree()

    def run_delete(self):
        """Запрашивает значение и удаляет его из дерева."""
        if not self.tree:
            self._show_warning("Дерево пустое!")
            return

        value = self._get_user_input("Введите значение для удаления")
        if value is not None:
            if not BinaryTree.search(self.tree, value):
                self._show_warning("Значение не найдено!")
            else:
                self.tree = BinaryTree.delete(self.tree, value)
                self.draw_tree()

    def run_search(self):
        """Запрашивает значение и подсвечивает его в дереве."""
        if not self.tree:
            self._show_warning("Дерево пустое!")
            return

        value = self._get_user_input("Введите значение для поиска")
        if value is not None:
            if BinaryTree.search(self.tree, value):
                self.draw_tree(highlight_value=value)
            else:
                self._show_warning("Значение не найдено!")

    def _get_user_input(self, title):
        """Отображает диалог ввода значения."""
        try:
            return int(simpledialog.askstring(title, "Введите целое число:"))
        except (TypeError, ValueError):
            return None

    def _show_warning(self, message):
        """Отображает предупреждающее сообщение."""
        messagebox.showwarning("Внимание", message)

    def draw_tree(self, highlight_value=None):
        """Отрисовывает дерево на холсте."""
        self.canvas.delete("all")
        if not self.tree:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0:
            return

        depth = BinaryTree.get_tree_depth(self.tree)
        if depth <= 0:
            return

        # Автоматическая настройка параметров отрисовки
        max_levels = min(depth, self.max_display_depth)
        self.vertical_spacing = (canvas_height - 100) // (max_levels + 1)

        # Рассчитываем стартовую позицию
        start_x = canvas_width // 2
        start_y = 50 + self.node_radius

        # Рекурсивная отрисовка дерева
        self._draw_subtree(
            self.tree,
            start_x,
            start_y,
            self.horizontal_spacing * (2 ** (max_levels - 1)),
            max_levels,
            1,
            highlight_value
        )

    def _draw_subtree(self, node, x, y, spacing, max_depth, current_depth, highlight_value=None):
        """Рекурсивно отрисовывает поддерево."""
        if not node or current_depth > max_depth:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Отрисовка связей с потомками
        if node.left and current_depth < max_depth:
            left_x = x - spacing / 2
            left_y = y + self.vertical_spacing
            if self._is_visible(left_x, left_y):
                self.canvas.create_line(
                    x, y + self.node_radius,
                    left_x, left_y - self.node_radius,
                    fill='gray', width=2
                )
                self._draw_subtree(
                    node.left, left_x, left_y,
                    spacing / 2, max_depth,
                    current_depth + 1, highlight_value
                )

        if node.right and current_depth < max_depth:
            right_x = x + spacing / 2
            right_y = y + self.vertical_spacing
            if self._is_visible(right_x, right_y):
                self.canvas.create_line(
                    x, y + self.node_radius,
                    right_x, right_y - self.node_radius,
                    fill='gray', width=2
                )
                self._draw_subtree(
                    node.right, right_x, right_y,
                    spacing / 2, max_depth,
                    current_depth + 1, highlight_value
                )

        # Отрисовка узла
        fill_color = 'lightgreen' if highlight_value == node.value else 'lightblue'
        self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill=fill_color, outline='black', width=2
        )
        self.canvas.create_text(
            x, y,
            text=str(node.value),
            font=('Arial', 10, 'bold'),
            fill='black'
        )

    def _is_visible(self, x, y):
        """Проверяет, находится ли точка в видимой области холста."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return (
                self.node_radius <= x <= canvas_width - self.node_radius and
                self.node_radius <= y <= canvas_height - self.node_radius
        )


def main():
    """Точка входа в приложение."""
    root = tk.Tk()
    app = BinaryTreeVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()