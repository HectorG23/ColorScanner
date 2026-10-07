import tkinter.colorchooser as colorchooser

import cv2
import customtkinter as ctk
import pyperclip
from PIL import Image, ImageTk

from core.color_logic import identify_color, rgb_to_hex
from ui.color_map_3d import ColorMap3D


class ColorScanner(ctk.CTk):
    """Interfaz de escritorio para explorar y guardar colores RGB."""

    BG = "#090D16"
    PANEL = "#111827"
    CARD = "#182235"
    ACCENT = "#42E8D5"
    TEXT = "#F1F5F9"
    MUTED = "#94A3B8"

    def __init__(self):
        super().__init__()
        self.title("ColorScanner | Neon Color Detector")
        self.geometry("1180x780")
        self.minsize(920, 640)
        self.configure(fg_color=self.BG)
        ctk.set_appearance_mode("dark")

        self.font_size = 14
        self.current_rgb = (0, 0, 0)
        self.cards = []
        self.camera_ready = False
        self.cap = cv2.VideoCapture(0)
        self.camera_ready = self.cap.isOpened()
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_camera_panel()
        self._build_inspector_panel()
        self._build_color_map()
        self._set_camera_status()
        self.update_video()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(brand, text="◈", text_color=self.ACCENT,
                     font=ctk.CTkFont(size=30, weight="bold")).pack(side="left", padx=(0, 10))
        title_box = ctk.CTkFrame(brand, fg_color="transparent")
        title_box.pack(side="left")
        ctk.CTkLabel(title_box, text="COLORSCANNER",
                     font=ctk.CTkFont(size=23, weight="bold"), text_color=self.TEXT).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Explora el color que tienes delante",
                     font=ctk.CTkFont(size=12), text_color=self.MUTED).pack(anchor="w")

        tools = ctk.CTkFrame(header, fg_color=self.PANEL, corner_radius=14)
        tools.grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(tools, text="TEXTO", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=self.MUTED).pack(side="left", padx=(12, 5), pady=8)
        ctk.CTkButton(tools, text="A−", width=38, height=34, corner_radius=10,
                      fg_color=self.CARD, hover_color="#26354D", command=lambda: self.change_font_size(-1)
                      ).pack(side="left", padx=3, pady=6)
        self.font_size_value = ctk.CTkLabel(tools, text=str(self.font_size), width=25,
                                            font=ctk.CTkFont(size=12), text_color=self.TEXT)
        self.font_size_value.pack(side="left")
        ctk.CTkButton(tools, text="A+", width=38, height=34, corner_radius=10,
                      fg_color=self.CARD, hover_color="#26354D", command=lambda: self.change_font_size(1)
                      ).pack(side="left", padx=(3, 10), pady=6)

    def _build_camera_panel(self):
        self.video_frame = ctk.CTkFrame(self, fg_color=self.PANEL, corner_radius=22,
                                        border_width=1, border_color="#26354D")
        self.video_frame.grid(row=1, column=0, padx=(24, 10), pady=(8, 22), sticky="nsew")
        self.video_frame.grid_rowconfigure(1, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 6))
        ctk.CTkLabel(top, text="◉  LECTOR EN VIVO", text_color=self.TEXT,
                     font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        self.camera_badge = ctk.CTkLabel(top, text="●  Buscando cámara…", text_color=self.MUTED,
                                         font=ctk.CTkFont(size=11))
        self.camera_badge.pack(side="right")

        self.video_label = ctk.CTkLabel(self.video_frame, text="", fg_color="#070A10",
                                        corner_radius=16)
        self.video_label.grid(row=1, column=0, sticky="nsew", padx=16, pady=(6, 12))

        footer = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 16))
        footer.grid_columnconfigure(0, weight=1)
        self.live_color = ctk.CTkLabel(footer, text="●  #000000   RGB 0, 0, 0",
                                       text_color=self.TEXT, font=ctk.CTkFont(size=12, family="Consolas"))
        self.live_color.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(footer, text="Apunta la mira al color que quieres leer",
                     text_color=self.MUTED, font=ctk.CTkFont(size=11)).grid(row=0, column=1, sticky="e")

    def _build_inspector_panel(self):
        self.inspector = ctk.CTkFrame(self, fg_color=self.PANEL, corner_radius=22,
                                      border_width=1, border_color="#26354D")
        self.inspector.grid(row=1, column=1, padx=(10, 24), pady=(8, 22), sticky="nsew")
        self.inspector.grid_columnconfigure(0, weight=1)
        self.inspector.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self.inspector, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(17, 8))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="✦  TUS COLORES", text_color=self.TEXT,
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w")
        self.count_label = ctk.CTkLabel(header, text="0 muestras", text_color=self.MUTED,
                                        font=ctk.CTkFont(size=11))
        self.count_label.grid(row=0, column=1, sticky="e")

        actions = ctk.CTkFrame(self.inspector, fg_color="transparent")
        actions.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        self.btn_capture = ctk.CTkButton(actions, text="●  Escanear", height=42,
                                         corner_radius=12, font=ctk.CTkFont(size=13, weight="bold"),
                                         fg_color=self.ACCENT, text_color="#071015",
                                         hover_color="#2CC6B5", command=self.capture_current_color)
        self.btn_capture.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(actions, text="🎨  Elegir", height=42, corner_radius=12,
                      font=ctk.CTkFont(size=13, weight="bold"), fg_color=self.CARD,
                      hover_color="#26354D", command=self.pick_color).grid(row=0, column=1,
                                                                           sticky="ew", padx=(5, 0))

        self.scroll_history = ctk.CTkScrollableFrame(self.inspector, fg_color="transparent",
                                                      scrollbar_button_color="#334155")
        self.scroll_history.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 2))
        self.empty_hint = ctk.CTkLabel(self.scroll_history,
                                       text="Aún no hay muestras\n\nEscanea la cámara o elige un color para empezar.",
                                       text_color=self.MUTED, justify="center",
                                       font=ctk.CTkFont(size=self.font_size))
        self.empty_hint.pack(expand=True, fill="both", pady=22)

        self.copy_status = ctk.CTkLabel(self.inspector, text="",
                                        text_color=self.ACCENT, font=ctk.CTkFont(size=11))
        self.copy_status.grid(row=3, column=0, sticky="w", padx=18, pady=(0, 8))

        self.map_frame = ctk.CTkFrame(self.inspector, fg_color="#0B111C", corner_radius=16, height=205)
        self.map_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.map_frame.grid_propagate(False)

    def _build_color_map(self):
        self.color_chart = ColorMap3D(self.map_frame)

    def _set_camera_status(self):
        if self.camera_ready:
            self.camera_badge.configure(text="●  Cámara conectada", text_color=self.ACCENT)
            self.btn_capture.configure(state="normal")
        else:
            self.camera_badge.configure(text="●  Sin cámara", text_color="#FBBF24")
            self.btn_capture.configure(state="disabled")
            self.video_label.configure(
                text="▣\n\nCÁMARA NO DISPONIBLE\nConecta una cámara o elige un color manualmente",
                text_color=self.MUTED, font=ctk.CTkFont(size=self.font_size, weight="bold"))

    def update_video(self):
        if self.camera_ready:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                cx, cy = width // 2, height // 2
                pixel = frame[cy, cx]
                self.current_rgb = (int(pixel[2]), int(pixel[1]), int(pixel[0]))
                cv2.rectangle(frame, (cx - 30, cy - 30), (cx + 30, cy + 30), (0, 251, 255), 2)
                cv2.line(frame, (cx - 42, cy), (cx + 42, cy), (0, 251, 255), 1)
                cv2.line(frame, (cx, cy - 42), (cx, cy + 42), (0, 251, 255), 1)
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image.thumbnail((1200, 900), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=image)
                self.video_label.img_tk = photo
                self.video_label.configure(image=photo, text="")
                hex_value = rgb_to_hex(self.current_rgb)
                self.live_color.configure(text=f"●  {hex_value}   RGB {self.current_rgb[0]}, {self.current_rgb[1]}, {self.current_rgb[2]}")
            else:
                self.camera_ready = False
                self._set_camera_status()
        self.after(30, self.update_video)

    def capture_current_color(self):
        if self.camera_ready:
            self.add_color_sample(self.current_rgb)

    def pick_color(self):
        _color, hex_value = colorchooser.askcolor(parent=self, title="Elige un color")
        if hex_value:
            hex_value = hex_value.lstrip("#")
            rgb = tuple(int(hex_value[index:index + 2], 16) for index in (0, 2, 4))
            self.add_color_sample(rgb)

    def add_color_sample(self, rgb):
        hex_value = rgb_to_hex(rgb)
        name = identify_color(rgb)
        if hasattr(self, "empty_hint") and self.empty_hint.winfo_exists():
            self.empty_hint.destroy()
        card = ctk.CTkFrame(self.scroll_history, fg_color=self.CARD, corner_radius=13)
        card.pack(fill="x", padx=3, pady=4)
        card.grid_columnconfigure(1, weight=1)
        swatch = ctk.CTkFrame(card, width=38, height=38, corner_radius=12, fg_color=hex_value)
        swatch.grid(row=0, column=0, rowspan=2, padx=11, pady=10)
        swatch.grid_propagate(False)
        name_label = ctk.CTkLabel(card, text=name.title(), anchor="w", text_color=self.TEXT,
                                  font=ctk.CTkFont(size=self.font_size, weight="bold"))
        name_label.grid(row=0, column=1, sticky="ew", padx=(0, 5), pady=(7, 0))
        hex_label = ctk.CTkLabel(card, text=hex_value, anchor="w", text_color=self.MUTED,
                                 font=ctk.CTkFont(size=max(10, self.font_size - 2), family="Consolas"))
        hex_label.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 7))
        copy_button = ctk.CTkButton(card, text="⧉", width=36, height=34, corner_radius=10,
                                    fg_color="#26354D", hover_color="#354967",
                                    font=ctk.CTkFont(size=16), command=lambda value=hex_value: self.copy_to_clipboard(value))
        copy_button.grid(row=0, column=2, rowspan=2, padx=10)
        self.cards.append((name_label, hex_label))
        self.count_label.configure(text=f"{len(self.cards)} muestra" + ("s" if len(self.cards) != 1 else ""))
        self.color_chart.add_color_point(rgb, hex_value)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        self.copy_status.configure(text=f"✓  {text} copiado al portapapeles")
        self.after(1800, lambda: self.copy_status.configure(text="") if self.copy_status.winfo_exists() else None)

    def change_font_size(self, delta):
        self.font_size = max(11, min(22, self.font_size + delta))
        self.font_size_value.configure(text=str(self.font_size))
        for name_label, hex_label in self.cards:
            name_label.configure(font=ctk.CTkFont(size=self.font_size, weight="bold"))
            hex_label.configure(font=ctk.CTkFont(size=max(10, self.font_size - 2), family="Consolas"))
        if self.empty_hint.winfo_exists():
            self.empty_hint.configure(font=ctk.CTkFont(size=self.font_size))
        if not self.camera_ready:
            self.video_label.configure(font=ctk.CTkFont(size=self.font_size, weight="bold"))

    def close_app(self):
        if self.cap is not None:
            self.cap.release()
        self.destroy()
