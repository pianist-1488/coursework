import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ApproximationWindow(tk.Toplevel):
    def __init__(self, parent, slope, intercept, x_data, y_data, x_value):
        super().__init__(parent)
        self.title("Аппроксимирующая функция")
        self.geometry("500x500")
        self.configure(bg="#FFCC99")

        self.label1 = tk.Label(self, text=f"Аппроксимирующая функция: y = {slope:.2f} * x + ({intercept:.2f})", bg="#FFCC99")
        self.label1.pack(pady=5)

        self.label2 = tk.Label(self, text="", bg="#FFCC99")
        self.label2.pack(pady=5)

        self.button_back = tk.Button(self, text="Назад", command=self.back)
        self.button_back.pack(pady=5)

        self.slope = slope
        self.intercept = intercept
        self.x_data = x_data
        self.y_data = y_data

        self.plot_graph()

        if x_value is not None:
            y_value = self.slope * x_value + self.intercept
            self.label2.config(text=f"При x={x_value}, значение аппроксимирующей функции = {y_value:.2f}")

    def plot_graph(self):
        fig, ax = plt.subplots()
        ax.scatter(self.x_data, self.y_data, label="Data Points")
        x = np.array(self.x_data)
        y = self.slope * x + self.intercept
        ax.plot(x, y, label="Approximation Line", color="red")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def back(self):
        self.destroy()
        self.master.deiconify()
