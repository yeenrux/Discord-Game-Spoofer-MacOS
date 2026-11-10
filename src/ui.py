import tkinter as tk
import queue
import threading
from tkinter import ttk
from .games import fetch
from .build import spoof

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spoofer")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        self.events = queue.Queue()
        self.games = []
        self.selected = tk.StringVar()
        self.status = tk.StringVar(value="Loading...")

        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Game").pack(anchor="w")
        self.combo = ttk.Combobox(frame, textvariable=self.selected, state="disabled")
        self.combo.pack(fill="x", pady=(4, 10))
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x")
        self.spoof_button = ttk.Button(buttons, text="Spoof", command=self.spoof, state="disabled")
        self.spoof_button.pack(side="left")
        ttk.Label(frame, textvariable=self.status, wraplength=325).pack(anchor="w", pady=(10, 0))
        self.root.after(100, self.poll)
        self.task("games", fetch)

    def task(self, kind, callback, *args):
        def work():
            self.events.put((kind, callback(*args)))
        threading.Thread(target=work, daemon=True).start()

    def spoof(self):
        index = self.combo.current()
        if index < 0 or index >= len(self.games):
            return
        name, game_id = self.games[index]
        self.status.set("Please wait...")
        self.task("spoof", spoof, name, game_id)

    def poll(self):
        try:
            while True:
                kind, result = self.events.get_nowait()
                if kind == "games":
                    self.games = result
                    self.combo["values"] = [name for name, _ in result]
                    if result:
                        self.combo.current(0)
                        self.combo.configure(state="readonly")
                        self.spoof_button.configure(state="normal")
                    self.status.set("")
                elif kind == "spoof":
                    self.status.set("Done")
        except queue.Empty:
            pass
        self.root.after(100, self.poll)