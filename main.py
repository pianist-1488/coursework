import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ApproximationWindow import ApproximationWindow


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Курсовая работа")
        self.configure(bg="#FFCC99")
        self.geometry("600x700")

        tk.Label(self, text="Введите количество точек", bg="#FFCC99").pack(pady=5)
        self.textbox = tk.Entry(self)
        self.textbox.pack()

        self.button1 = tk.Button(self, text="Ввод координат", command=self.input_coordinates)
        self.button1.pack(pady=5)

        self.data_frame = tk.Frame(self, bg="#FFCC99")
        self.data_frame.pack()

        self.tree = ttk.Treeview(self.data_frame, columns=("n", "x", "y"), show="headings")
        self.tree.heading("n", text="n")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")
        self.tree.pack()

        self.tree.bind('<Double-1>', self.on_double_click)

        self.button2 = tk.Button(self, text="Построить график", command=self.plot_graph)
        self.button2.pack(pady=5)

        tk.Label(self, text="Введите значение X, для которого хотите определить значение аппроксимирующей функции:",
                 bg="#FFCC99").pack(pady=5)
        self.entry_x = tk.Entry(self)
        self.entry_x.pack(pady=5)

        self.canvas_frame = tk.Frame(self, bg="#FFCC99")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = None

        self.button3 = tk.Button(self, text="Построить аппроксимирующую прямую", command=self.show_approximation)
        self.button3.pack(pady=5)

    def input_coordinates(self):
        self.tree.delete(*self.tree.get_children())
        try:
            n = int(self.textbox.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введено некорректное количество точек")
            return

        if n >= 2:
            for i in range(n):
                self.tree.insert("", "end", values=(i + 1, "", ""))
        else:
            messagebox.showerror("Ошибка", "Нельзя найти аппроксимирующую функцию по одной точке")

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            row = self.tree.identify_row(event.y)

            x, y, width, height = self.tree.bbox(row, column)

            entry = tk.Entry(self.data_frame)
            entry.place(x=x, y=y, width=width, height=height)
            entry.focus()

            def on_focus_out(event):
                self.tree.set(row, column=column, value=entry.get())
                entry.destroy()

            entry.bind("<FocusOut>", on_focus_out)
            entry.bind("<Return>", on_focus_out)

    def plot_graph(self):
        x_data = []
        y_data = []

        for child in self.tree.get_children():
            _, x, y = self.tree.item(child)["values"]
            try:
                x = float(x)
                y = float(y)
            except ValueError:
                messagebox.showerror("Ошибка", "Вы не ввели данные")
                return
            x_data.append(x)
            y_data.append(y)

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots()
        ax.scatter(x_data, y_data, label="Data Points")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_approximation(self):
        x_value = self.entry_x.get()
        try:
            x_value = float(x_value)
        except ValueError:
            x_value = None

        n = len(self.tree.get_children())
        x_data = []
        y_data = []

        for child in self.tree.get_children():
            _, x, y = self.tree.item(child)["values"]
            x_data.append(float(x))
            y_data.append(float(y))

        x = np.array(x_data)
        y = np.array(y_data)

        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

        self.approximation_window = ApproximationWindow(self, m, c, x_data, y_data, x_value)
        self.withdraw()
        self.approximation_window.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
