import json
import os

# Cargar la base de datos una sola vez al importar el módulo
COLORS_DB = {}
json_path = os.path.join(os.path.dirname(__file__), 'colors.json')

try:
    with open(json_path, 'r') as f:
        COLORS_DB = json.load(f)
except FileNotFoundError:
    # Backup por si el archivo no existe
    COLORS_DB = {"Negro": "#000000", "Blanco": "#FFFFFF"}

def rgb_to_hex(rgb):
    """Convierte una tupla (r, g, b) a un string hexadecimal #RRGGBB"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]).upper()

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def identify_color(rgb_escaneado):
    r1, g1, b1 = rgb_escaneado
    min_dist = float('inf')
    nombre_cercano = "Desconocido"

    # Iteramos sobre CUALQUIER cantidad de colores que tenga el JSON
    for nombre, hex_code in COLORS_DB.items():
        r2, g2, b2 = hex_to_rgb(hex_code)
        
        # Matemáticas: Distancia en el espacio 3D RGB
        distancia = ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)**0.5
        
        if distancia < min_dist:
            min_dist = distancia
            nombre_cercano = nombre

    return nombre_cercano