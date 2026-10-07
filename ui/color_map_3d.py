import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ColorMap3D:
    def __init__(self, parent):
        # Crear la figura de Matplotlib
        self.fig = plt.figure(figsize=(4, 4), facecolor='#121212')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#121212')
        
        # Configurar límites y etiquetas (estilo neón)
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_zlim(0, 255)
        self.ax.set_xlabel('R', color='white')
        self.ax.set_ylabel('G', color='white')
        self.ax.set_zlabel('B', color='white')
        self.ax.tick_params(colors='gray')

        # Integrar en CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def add_color_point(self, rgb, hex_code):
        r, g, b = rgb
        # Dibujar un punto con el color real escaneado
        self.ax.scatter(r, g, b, c=hex_code, s=50, edgecolors='white', linewidth=0.5)
        self.canvas.draw()