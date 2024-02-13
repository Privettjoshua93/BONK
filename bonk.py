import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, StringVar, Radiobutton
import json
import random
import time
from threading import Thread
from PIL import Image, ImageTk
from playsound import playsound

SCHEDULE_ITEMS_NORMAL = [("Posture Check!", 20), ("Hydration Check!", 60), ("Posture Check!", 95), ("Hydration Check!", 125), ("Mindfulness Reminder!", 150), ("Posture Check!", 175), ("Posture Check!", 210), ("Hydration Check!", 235), ("Posture Check!", 255), ("Hydration Check!", 285), ("Mindfulness Reminder!", 310), ("Posture Check!", 355)]
SCHEDULE_ITEMS_FAST = [("Posture Check!", 1), ("Hydration Check!", 2), ("Posture Check!", 3), ("Hydration Check!", 4),("Mindfulness Reminder!", 5), ("Posture Check!", 165), ("Posture Check!", 195), ("Hydration Check!", 225), ("Posture Check!", 245), ("Hydration Check!", 275), ("Mindfulness Reminder!", 300), ("Posture Check!", 345)]
SCHEDULE_ITEMS_SLOW = [("Posture Check!", 35), ("Hydration Check!", 70), ("Posture Check!", 115), ("Hydration Check!", 135), ("Mindfulness Reminder!", 165), ("Posture Check!", 190), ("Posture Check!", 225), ("Hydration Check!", 255), ("Posture Check!", 315), ("Hydration Check!", 345), ("Mindfulness Reminder!", 380), ("Posture Check!", 415)]
IMAGES = [r"D:\Bonk\v9.00\images\compassion.png", r"D:\Bonk\v9.00\images\field.png", r"D:\Bonk\v9.00\images\grouphug.png", r"D:\Bonk\v9.00\images\thinking.png", r"D:\Bonk\v9.00\images\watchful.png"]
AFFIRMATIONS_FILE = r"D:\Bonk\v9.00\affirmations.json"
APP_TITLE = "BONK!"
ICON_PATH = r"D:\Bonk\v9.00\bonk.ico"
SOUNDS = {"Posture Check!": r"D:\Bonk\v9.00\sounds\posture.wav", "Hydration Check!": r"D:\Bonk\v9.00\sounds\hydration.wav", "Mindfulness Reminder!": r"D:\Bonk\v9.00\sounds\mindfulness.wav"}
DARK_BG_COLOR = "#333333"
DARK_TEXT_COLOR = "#FFFFFF"

def center_window(window, width=500, height=120):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int((screen_width - width) / 2)
    center_y = int((screen_height - height) / 2)
    window.geometry(f'{width}x{height}+{center_x}+{center_y}')

def center_toplevel_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int((screen_width - width) / 2)
    center_y = int((screen_height - height) / 2)
    window.geometry(f'{width}x{height}+{center_x}+{center_y}')
def fade_away(window):
    alpha = window.attributes("-alpha")
    if alpha > 0:
        alpha -= 0.02
        window.attributes("-alpha", alpha)
        window.after(50, lambda: fade_away(window))
    else:
        window.destroy()

def explode(window, success_label):
    particles = []
    for _ in range(10):  
        x, y = 0, 0
        particle = Label(window, text="*", font=("Helvetica", 24), bg=DARK_BG_COLOR, fg="yellow")
        particle.place(x=x, y=y)
        particles.append(particle)
    move_particles(window, particles, 20, 0)  

def move_particles(window, particles, step, iteration):
    if iteration < 15:  
        for particle in particles:
            x, y = particle.place_info()['x'], particle.place_info()['y']
            new_x = int(x) + random.randint(-step, step)
            new_y = int(y) + random.randint(-step, step)
            particle.place(x=new_x, y=new_y)
        window.after(100, lambda: move_particles(window, particles, step, iteration + 1))
    else:
        for particle in particles:
            particle.destroy()
        fade_away(window)  

def show_mindfulness_game(affirmation):
    game_window_width = 600
    game_window_height = 300
    
    game_window = Toplevel(app)
    game_window.title(APP_TITLE)
    game_window.iconbitmap(ICON_PATH)
    game_window.attributes("-topmost", True)
    game_window.configure(bg=DARK_BG_COLOR)
    game_window.grab_set()
    center_toplevel_window(game_window, game_window_width, game_window_height)
    
    instructions = Label(game_window, text="Please type the affirmation below:", font=("Helvetica", 14), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
    instructions.pack(pady=(20, 10))
    
    affirmation_label = Label(game_window, text=affirmation, font=("Helvetica", 14), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
    affirmation_label.pack()
    
    entry = Entry(game_window, font=("Helvetica", 14), width=50)
    entry.pack(pady=20)

    def check_entry():
        user_text = entry.get().strip()
        if user_text:
            success_label = Label(game_window, text="Congratulations, keep going!", font=("Helvetica", 14), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
            success_label.pack()
            complete_button.config(state="disabled")
            entry.config(state="disabled")
            explode(game_window, success_label)  
        else:
            error_label = Label(game_window, text="Please enter an affirmation to continue.", font=("Helvetica", 14), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
            error_label.pack()

    complete_button = Button(game_window, text="Complete", command=check_entry)
    complete_button.pack(pady=(0, 10))

    entry.focus_set()

def show_notification(title, image_path, sound_path):
    if title == "Mindfulness Reminder!":
        with open(AFFIRMATIONS_FILE, "r") as file:
            affirmations = json.load(file)["affirmations"]
            affirmation = random.choice(affirmations)
        show_mindfulness_game(affirmation)
    else:
        notification_window = Toplevel(app)
        notification_window.title(APP_TITLE)
        notification_window.iconbitmap(ICON_PATH)
        notification_window.attributes("-topmost", True)
        notification_window.configure(bg=DARK_BG_COLOR)
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        name_label = tk.Label(notification_window, text=title, font=("Helvetica", 16, "bold"), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
        name_label.pack(pady=(7, 0))
        notification_image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(notification_image)
        image_label = tk.Label(notification_window, image=photo_image, bg=DARK_BG_COLOR)
        image_label.image = photo_image
        image_label.pack(pady=(5, 4))
        image_width, image_height = notification_image.size
        window_width = image_width + 20
        window_height = image_height + 100
        position_x = screen_width - window_width - 10
        position_y = screen_height - window_height - 50
        notification_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        with open(AFFIRMATIONS_FILE, "r") as file:
            affirmations = json.load(file)["affirmations"]
            affirmation = random.choice(affirmations)
        affirmation_label = tk.Label(notification_window, text=affirmation, font=("Helvetica", 14), wraplength=window_width - 20, bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
        affirmation_label.pack(pady=(0, 0))
        Thread(target=lambda: playsound(sound_path), daemon=True).start()
        notification_window.after(12000, notification_window.destroy)

def schedule_notifications():
    schedule_idx = 0
    schedule_items = SCHEDULE_ITEMS_NORMAL
    SCHEDULE_LENGTH = sum(item[1] for item in schedule_items)
    start_time = time.time()
    while True:
        if speed_var.get() == "normal":
            schedule_items = SCHEDULE_ITEMS_NORMAL
        elif speed_var.get() == "fast":
            schedule_items = SCHEDULE_ITEMS_FAST
        elif speed_var.get() == "slow":
            schedule_items = SCHEDULE_ITEMS_SLOW
        elapsed_seconds = (time.time() - start_time)
        total_minutes = elapsed_seconds
        target_name, target_minutes = schedule_items[schedule_idx]
        if total_minutes >= target_minutes:
            image_path = random.choice(IMAGES)
            sound_path = SOUNDS[target_name]
            show_notification(target_name, image_path, sound_path)
            schedule_idx = (schedule_idx + 1) % len(schedule_items)
            if schedule_idx == 0:
                start_time = time.time()
        time.sleep(1)

app = tk.Tk()
app.title(APP_TITLE)
app.iconbitmap(ICON_PATH)
app.configure(bg=DARK_BG_COLOR)
app.geometry("500x120")
label = tk.Label(app, text="You may minimize this window - we will continue to run in the background.", font=("Helvetica", 10,), bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR)
label.pack(pady=(20, 0))
speed_var = StringVar(value="normal")

for text, value in [("Slow", "slow"), ("Normal", "normal"), ("Fast", "fast")]:
    Radiobutton(app, text=text, variable=speed_var, value=value, bg=DARK_BG_COLOR, fg=DARK_TEXT_COLOR, selectcolor=DARK_BG_COLOR).pack(side=tk.LEFT)

notification_thread = Thread(target=schedule_notifications, daemon=True)
notification_thread.start()
center_window(app, 500, 120)
app.mainloop()