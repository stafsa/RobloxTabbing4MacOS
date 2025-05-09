import tkinter as tk
from tkinter import Toplevel, Label, StringVar
import psutil
import os
import signal
import json
from threading import Thread
from pynput import keyboard

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
default_settings = {"freeze_key": "-"}

os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(default_settings, f, indent=4)

with open(SETTINGS_FILE, "r") as f:
    settings = json.load(f)

freeze_key = settings.get("freeze_key", "-")

roblox_pid = None
is_frozen = False

def get_roblox_pid():
    global roblox_pid
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "Roblox" in proc.info['name']:
                roblox_pid = proc.info['pid']
                return True
        except:
            continue
    return False

def freeze_roblox():
    global is_frozen
    if get_roblox_pid() and not is_frozen:
        os.kill(roblox_pid, signal.SIGSTOP)
        is_frozen = True

def unfreeze_roblox():
    global is_frozen
    if roblox_pid and is_frozen:
        os.kill(roblox_pid, signal.SIGCONT)
        is_frozen = False

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char == freeze_key and not is_frozen:
            freeze_roblox()
        elif hasattr(key, 'name') and key.name == freeze_key and not is_frozen:
            freeze_roblox()
    except:
        pass

def on_release(key):
    try:
        if hasattr(key, 'char') and key.char == freeze_key and is_frozen:
            unfreeze_roblox()
        elif hasattr(key, 'name') and key.name == freeze_key and is_frozen:
            unfreeze_roblox()
    except:
        pass

def run_key_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def open_settings():
    top = Toplevel()
    top.title("Settings")
    top.geometry("400x130")
    top.configure(bg="#C0C0C0")

    instruction = Label(top, text="Press a key to set as new freeze key:", font=("Arial", 12), bg="#C0C0C0")
    instruction.pack(pady=(10, 5))

    key_display = StringVar()
    key_display.set("[waiting for input]")
    display = Label(top, textvariable=key_display, font=("Arial", 14, "bold"), bg="#C0C0C0", fg="blue")
    display.pack(pady=(0, 10))

    def on_key_press(event):
        global freeze_key
        key = event.keysym.lower()
        key_display.set(f"Selected: {key}")
        freeze_key = key
        settings["freeze_key"] = freeze_key
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        top.after(700, top.destroy)

    top.bind("<Key>", on_key_press)

def create_gui():
    root = tk.Tk()
    root.title("RobloxTabbing4MacOS")
    root.geometry("500x200")
    root.resizable(False, False)
    root.configure(bg="#C0C0C0")
    root.attributes('-topmost', True)

    shadow = tk.Label(root, text="ROBLOXTABBING4MACOS", font=("Comic Sans MS", 20, "bold"), fg="gray20", bg="#C0C0C0")
    shadow.place(x=23, y=43)

    label = tk.Label(root, text="ROBLOXTABBING4MACOS", font=("Comic Sans MS", 20, "bold"), fg="blue", bg="#C0C0C0")
    label.place(x=20, y=40)

    status = tk.Label(root, text="is activated", font=("Comic Sans MS", 14), fg="black", bg="#C0C0C0")
    status.place(x=180, y=90)

    btn = tk.Button(root, text="Settings", command=open_settings, bg="#A0A0A0")
    btn.place(x=400, y=150)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()

Thread(target=run_key_listener, daemon=True).start()
create_gui()
