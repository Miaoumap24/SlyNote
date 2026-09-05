import os
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
import customtkinter as ctk

# Theme configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZenithNote(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SlyNote")
        self.geometry("1000°x650")
        self.minsize(800, 500)

        self.current_file = None
        self.zoom_level = 100

        self._init_ui()
        self._bind_shortcuts()
        self._update_status()

    def _init_ui(self):
        # --- Top Action Bar ---
        self.toolbar = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.toolbar.pack(side="top", fill="x")

        # File Operations
        self.btn_new = ctk.CTkButton(self.toolbar, text="New", width=70, command=self.new_file)
        self.btn_new.pack(side="left", padx=5, pady=8)

        self.btn_open = ctk.CTkButton(self.toolbar, text="Open", width=70, command=self.open_file)
        self.btn_open.pack(side="left", padx=5, pady=8)

        self.btn_save = ctk.CTkButton(self.toolbar, text="Save", width=70, command=self.save_file)
        self.btn_save.pack(side="left", padx=5, pady=8)

        # Formatting Options
        self.font_family = ctk.CTkOptionMenu(
            self.toolbar, 
            values=["Consolas", "Arial", "Courier New", "Segoe UI"],
            command=self._change_font
        )
        self.font_family.set("Consolas")
        self.font_family.pack(side="left", padx=15, pady=8)

        self.font_size = ctk.CTkOptionMenu(
            self.toolbar,
            values=[str(i) for i in range(8, 32, 2)],
            width=65,
            command=self._change_font
        )
        self.font_size.set("14")
        self.font_size.pack(side="left", padx=5, pady=8)

        # Theme Switcher
        self.theme_switch = ctk.CTkSwitch(self.toolbar, text="Dark Mode", command=self._toggle_theme)
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        self.theme_switch.pack(side="right", padx=15, pady=8)

        # --- Status Bar ---
        self.statusbar = ctk.CTkFrame(self, height=25, corner_radius=0)
        self.statusbar.pack(side="bottom", fill="x")

        self.lbl_status = ctk.CTkLabel(self.statusbar, text="Ready", anchor="w")
        self.lbl_status.pack(side="left", padx=10)

        self.lbl_pos = ctk.CTkLabel(self.statusbar, text="Ln 1, Col 0 | 100%", anchor="e")
        self.lbl_pos.pack(side="right", padx=10)

        # --- Main Text Area ---
        self.text_frame = ctk.CTkFrame(self, corner_radius=0)
        self.text_frame.pack(fill="both", expand=True)

        self.editor = tk.Text(
            self.text_frame,
            wrap="word",
            undo=True,
            maxundo=-1,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Consolas", 14),
            bg="#1a1a1a",
            fg="#f0f0f0",
            insertbackground="#ffffff"
        )
        self.editor.pack(fill="both", expand=True, padx=10, pady=10)

    def _bind_shortcuts(self):
        # Event binding for text changes & navigation
        self.editor.bind("<KeyRelease>", self._on_key_release)
        self.editor.bind("<Control-n>", lambda e: self.new_file())
        self.editor.bind("<Control-o>", lambda e: self.open_file())
        self.editor.bind("<Control-s>", lambda e: self.save_file())
        self.editor.bind("<Control-MouseWheel>", self._on_zoom)

    # --- Core File Methods ---
    def new_file(self):
        self.editor.delete("1.0", tk.END)
        self.current_file = None
        self.title("SlyNote - Untitled")
        self._update_status("New file created.")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.current_file = path
            self.title(f"SlyNote - {os.path.basename(path)}")
            self._update_status(f"Opened: {path}")

    def save_file(self):
        if not self.current_file:
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not path:
                return
            self.current_file = path

        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END + "-1c"))
        self.title(f"SlyNote - {os.path.basename(self.current_file)}")
        self._update_status("File saved successfully.")

    # --- UI Event Handlers ---
    def _change_font(self, _=None):
        family = self.font_family.get()
        size = int(self.font_size.get())
        self.editor.configure(font=(family, size))

    def _toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.editor.configure(bg="#1a1a1a", fg="#f0f0f0", insertbackground="#ffffff")
        else:
            ctk.set_appearance_mode("Light")
            self.editor.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")

    def _on_zoom(self, event):
        # Dynamic font scaling via Ctrl + Wheel
        current_size = int(self.font_size.get())
        if event.delta > 0 and current_size < 40:
            current_size += 1
        elif event.delta < 0 and current_size > 8:
            current_size -= 1
        self.font_size.set(str(current_size))
        self._change_font()

    def _on_key_release(self, _=None):
        # Live updates for cursor position & line/col tracking
        cursor_pos = self.editor.index(tk.INSERT)
        line, col = cursor_pos.split(".")
        self.lbl_pos.configure(text=f"Ln {line}, Col {col} | Zoom {self.font_size.get()}pt")

    def _update_status(self, message="Ready"):
        self.lbl_status.configure(text=message)

if __name__ == "__main__":
    app = ZenithNote()
    app.mainloop()