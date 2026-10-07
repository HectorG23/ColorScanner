# ◈ ColorScanner

### Neon Color Detector Pro · Identificación de colores con cámara y selector manual

> Apunta la mira al color, captura una muestra y explora su posición en el espacio RGB.

**Python** · **CustomTkinter** · **OpenCV** · **Matplotlib**

<details open>
<summary>🖥️ Captura de la aplicación</summary>

La captura se carga desde [`assets/screenshot.jpg`](assets/screenshot.jpg) con una etiqueta HTML `<img>`:

<img src="assets/screenshot.jpg" alt="Interfaz de ColorScanner con lector en vivo y muestras de colores" width="100%">

</details>

<details open>
<summary>✨ Qué puedes hacer</summary>

- **Leer un color en vivo** desde la cámara y ver una mira sobre el centro del vídeo.
- **Elegir un color manualmente** con el selector del sistema cuando no hay cámara o quieres probar un valor concreto.
- Ver el nombre más parecido, el color de muestra, RGB y su código **HEX**.
- Copiar un código HEX con un botón de un toque.
- Explorar las muestras en el **mapa 3D RGB**.
- Cambiar el tamaño del texto de las muestras con **A− / A+**.
- Ver el estado de la cámara y el total de muestras de la sesión.

</details>

<details>
<summary>🧭 Cómo funciona</summary>

1. `main.py` inicia la ventana `ColorScanner`.
2. OpenCV intenta abrir el dispositivo de cámara `0`. Si no está disponible, la app informa el estado y mantiene habilitado el selector manual.
3. Para vídeo disponible, cada fotograma se voltea horizontalmente. La app lee el píxel central (OpenCV entrega BGR y se convierte a RGB) y dibuja la mira.
4. Al escanear o elegir un valor manual, la lógica convierte RGB a HEX y compara la muestra contra `core/colors.json`.
5. La app guarda la muestra en el historial de la sesión y añade un punto al mapa 3D.
6. El control de fuente cambia dinámicamente el tamaño de texto en las tarjetas del historial.

El nombre se elige mediante la distancia euclídea entre canales RGB:

```text
d = √((R1 − R2)² + (G1 − G2)² + (B1 − B2)²)
```

La distancia RGB es sencilla y rápida, pero no perceptual: la iluminación y las diferencias entre la percepción humana y el espacio RGB pueden alterar el nombre más cercano.

</details>

<details>
<summary>🏗️ Arquitectura</summary>

```mermaid
flowchart LR
    A[main.py] --> B[ui/main_window.py]
    B --> C[OpenCV cámara]
    B --> D[core/color_logic.py]
    D --> E[core/colors.json]
    B --> F[Historial y portapapeles]
    B --> G[ui/color_map_3d.py]
    G --> H[Matplotlib 3D]
```

| Archivo | Responsabilidad |
| --- | --- |
| `main.py` | Punto de entrada; crea la ventana y ejecuta el ciclo de CustomTkinter. |
| `ui/main_window.py` | Interfaz, cámara, mira, selector manual, historial, copia al portapapeles y controles de fuente. |
| `ui/color_map_3d.py` | Gráfico 3D de los canales rojo, verde y azul, integrado en Tkinter. |
| `core/color_logic.py` | Conversión RGB/HEX y búsqueda del nombre de color más cercano. |
| `core/colors.json` | Catálogo editable de colores con valores HEX. |
| `requeriments.txt` | Dependencias Python declaradas actualmente. |

</details>

<details>
<summary>🧰 Librerías y tecnologías</summary>

| Paquete / módulo | Uso |
| --- | --- |
| Python | Lenguaje de la aplicación. |
| `opencv-python` (`cv2`) | Captura de cámara, transformación de fotogramas y dibujo de la mira. |
| `customtkinter` | Ventana de escritorio y controles con tema oscuro. |
| `pillow` (`PIL`) | Conversión de fotogramas a imágenes Tkinter. |
| `numpy` | Operaciones numéricas y dependencia del ecosistema OpenCV/Matplotlib; el módulo del gráfico la importa, aunque no utiliza sus funciones directamente. |
| `pyperclip` | Copia de HEX al portapapeles. |
| `matplotlib` | Visualización tridimensional y puente `FigureCanvasTkAgg`. |
| JSON y biblioteca estándar | Carga de la paleta y utilidades del programa. |

</details>

<details>
<summary>🚀 Instalación y ejecución</summary>

Requiere Python 3.10 o posterior y, para lecturas en vivo, una cámara accesible al sistema.

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requeriments.txt matplotlib
python main.py
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requeriments.txt matplotlib
python main.py
```

> **Nombre del manifiesto:** el archivo actual se llama `requeriments.txt` (con esa ortografía). Incluye las dependencias necesarias, entre ellas Matplotlib. Para seguir la convención habitual de Python, puedes renombrarlo a `requirements.txt` y actualizar este comando.

</details>

<details>
<summary>🎮 Uso</summary>

1. Inicia `python main.py` desde la carpeta raíz.
2. Para leer la cámara, coloca un objeto bajo la mira y pulsa **● Escanear**.
3. Si no hay cámara, pulsa **🎨 Elegir** y selecciona un color del diálogo.
4. Usa **⧉** para copiar el HEX de una muestra.
5. Pulsa **A− / A+** para ajustar la tipografía del historial.

Las muestras y puntos del gráfico viven solo mientras la aplicación está abierta. El código revisado no guarda lecturas ni transmite vídeo.

</details>

<details>
<summary>🛠️ Límites y mejoras posibles</summary>

- La cámara predeterminada es el índice `0`; no hay selector de varios dispositivos.
- El escaneo usa un solo píxel central; un promedio de una región toleraría mejor ruido y variaciones.
- La búsqueda RGB no compensa iluminación ni percepción cromática.
- No hay persistencia ni exportación del historial.
- No se encontró una licencia. Añade una después de decidir cómo quieres distribuir el proyecto.

</details>

---

**GitHub:** `README.md` es la portada del repositorio. Ambos documentos usan la ruta relativa `assets/screenshot.jpg`; GitHub puede mostrar la captura directamente desde el repositorio.

