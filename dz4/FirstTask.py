import tkinter as tk
from tkinter import messagebox
import time


class BalancedTreeVisualizer:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.balance = 0  # -1, 0, 1
            self.x = 0
            self.y = 0

    def __init__(self, root):
        self.root_node = None
        self.tall = False
        self.animation_speed = 500  # мс задержки между шагами

        # Настройка GUI
        self.root = root
        self.root.title("Balanced Tree Visualizer")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Панель управления
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.entry = tk.Entry(control_frame, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Insert", command=self.insert_step).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Auto Insert", command=self.auto_insert).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Clear", command=self.clear_tree).pack(side=tk.LEFT, padx=5)

        # Статус
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(fill=tk.X)

    def set_status(self, text):
        self.status.config(text=text)
        self.root.update()

    def clear_tree(self):
        self.canvas.delete("all")
        self.root_node = None
        self.set_status("Tree cleared")

    def insert_step(self):
        try:
            key = int(self.entry.get())
            self.set_status(f"Inserting {key}...")
            self.root_node = self._insert(self.root_node, key, animate=True)
            self.entry.delete(0, tk.END)
            self.set_status(f"Inserted {key}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def auto_insert(self):
        keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
        for key in keys:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(key))
            self.insert_step()
            time.sleep(0.7)

    def _insert(self, node, key, animate=False):
        if node is None:
            if animate:
                self.set_status(f"Creating new node with key {key}")
                self.root.after(self.animation_speed)
            new_node = self.Node(key)
            if animate:
                self.draw_tree()
                self.highlight_node(new_node, "green")
                self.root.after(self.animation_speed)
            self.tall = True
            return new_node

        if animate:
            self.highlight_node(node, "yellow")
            self.set_status(f"Checking node {node.key}")
            self.root.after(self.animation_speed)

        if key < node.key:
            if animate:
                self.set_status(f"{key} < {node.key}, going left")
                self.root.after(self.animation_speed)
            node.left = self._insert(node.left, key, animate)
            if self.tall:
                if node.balance == 1:
                    node.balance = 0
                    self.tall = False
                elif node.balance == 0:
                    node.balance = -1
                    if animate:
                        self.set_status(f"Adjusting balance of {node.key} to -1")
                        self.root.after(self.animation_speed)
                else:
                    if animate:
                        self.set_status(f"Need to balance left-heavy {node.key}")
                        self.root.after(self.animation_speed)
                    node = self._balance_left(node)
                    self.tall = False
        elif key > node.key:
            if animate:
                self.set_status(f"{key} > {node.key}, going right")
                self.root.after(self.animation_speed)
            node.right = self._insert(node.right, key, animate)
            if self.tall:
                if node.balance == -1:
                    node.balance = 0
                    self.tall = False
                elif node.balance == 0:
                    node.balance = 1
                    if animate:
                        self.set_status(f"Adjusting balance of {node.key} to +1")
                        self.root.after(self.animation_speed)
                else:
                    if animate:
                        self.set_status(f"Need to balance right-heavy {node.key}")
                        self.root.after(self.animation_speed)
                    node = self._balance_right(node)
                    self.tall = False
        else:
            if animate:
                self.set_status(f"Key {key} already exists")
                self.highlight_node(node, "red")
                self.root.after(self.animation_speed)
            self.tall = False

        if animate:
            self.draw_tree()
            self.root.after(self.animation_speed)

        return node

    def _balance_left(self, node):
        left_child = node.left
        if left_child.balance == -1:
            # Single right rotation
            self.set_status(f"Single right rotation at {node.key}")
            node.left = left_child.right
            left_child.right = node
            node.balance = 0
            left_child.balance = 0
            return left_child
        else:
            # Double rotation (left-right)
            self.set_status(f"Double rotation (left-right) at {node.key}")
            right_grandchild = left_child.right
            left_child.right = right_grandchild.left
            right_grandchild.left = left_child
            node.left = right_grandchild.right
            right_grandchild.right = node

            if right_grandchild.balance == -1:
                node.balance = 1
                left_child.balance = 0
            elif right_grandchild.balance == 1:
                node.balance = 0
                left_child.balance = -1
            else:
                node.balance = 0
                left_child.balance = 0

            right_grandchild.balance = 0
            return right_grandchild

    def _balance_right(self, node):
        right_child = node.right
        if right_child.balance == 1:
            # Single left rotation
            self.set_status(f"Single left rotation at {node.key}")
            node.right = right_child.left
            right_child.left = node
            node.balance = 0
            right_child.balance = 0
            return right_child
        else:
            # Double rotation (right-left)
            self.set_status(f"Double rotation (right-left) at {node.key}")
            left_grandchild = right_child.left
            right_child.left = left_grandchild.right
            left_grandchild.right = right_child
            node.right = left_grandchild.left
            left_grandchild.left = node

            if left_grandchild.balance == 1:
                node.balance = -1
                right_child.balance = 0
            elif left_grandchild.balance == -1:
                node.balance = 0
                right_child.balance = 1
            else:
                node.balance = 0
                right_child.balance = 0

            left_grandchild.balance = 0
            return left_grandchild

    def draw_tree(self):
        self.canvas.delete("all")
        if self.root_node is None:
            return

        # Calculate positions
        self._calculate_positions(self.root_node, 400, 50, 200)

        # Draw connections first
        self._draw_connections(self.root_node)

        # Then draw nodes
        self._draw_nodes(self.root_node)

    def _calculate_positions(self, node, x, y, spacing):
        if node is None:
            return

        node.x = x
        node.y = y

        if node.left:
            self._calculate_positions(node.left, x - spacing, y + 80, spacing * 0.6)
        if node.right:
            self._calculate_positions(node.right, x + spacing, y + 80, spacing * 0.6)

    def _draw_connections(self, node):
        if node is None:
            return

        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, width=2, fill="gray")
            self._draw_connections(node.left)

        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, width=2, fill="gray")
            self._draw_connections(node.right)

    def _draw_nodes(self, node):
        if node is None:
            return

        # Draw node
        color = "lightblue"
        if node.balance == -1:
            color = "lightgreen"
        elif node.balance == 1:
            color = "lightcoral"

        self.canvas.create_oval(node.x - 20, node.y - 20, node.x + 20, node.y + 20, fill=color, outline="black")
        self.canvas.create_text(node.x, node.y, text=str(node.key), font=('Arial', 10, 'bold'))

        # Draw balance factor
        self.canvas.create_text(node.x, node.y + 25, text=str(node.balance), font=('Arial', 8))

        # Draw children
        self._draw_nodes(node.left)
        self._draw_nodes(node.right)

    def highlight_node(self, node, color):
        if node is None:
            return
        self.canvas.create_oval(node.x - 22, node.y - 22, node.x + 22, node.y + 22, outline=color, width=3)


if __name__ == "__main__":
    root = tk.Tk()
    app = BalancedTreeVisualizer(root)
    root.mainloop()