# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    logscreen.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ddivaev <ddivaev@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/11/23 09:14:17 by ddivaev           #+#    #+#              #
#    Updated: 2024/11/23 09:46:09 by ddivaev          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import subprocess
import sys
import time
import threading
import tkinter as tk
import psutil


LOCK_FILE = "./logscreen.lock"

def check_if_running():
    if os.path.exists(LOCK_FILE):
        print("Script is already running. Exiting.")
        sys.exit()
    else:
        # Create a lock file to indicate the script is running
        with open(LOCK_FILE, 'w') as f:
            f.write("locked")

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# Check if the script is already running
check_if_running()


class IdleTimerApp:
    def __init__(self):
        self.idle_time_threshold = 2 * 60  																						# TODO TIMER SET. SET AMOUNT OF SECONDS TO LOCK HERE
        self.last_input_time = time.time()
        self.locked = False
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.geometry("600x100")
        self.root.wait_visibility(self.root)
        self.root.wm_attributes("-alpha", 0.5)
        self.root.configure(bg="black")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"600x100+{screen_width // 2 - 300}+{screen_height - (screen_height)}")
        self.canvas = tk.Canvas(self.root, width=600, height=100, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.timer_text = self.canvas.create_text(300, 50, text="", font=("JetBrains Mono", 48), fill="white")					# TODO Change the font to your preffered font. I use JetBrains Mono
        threading.Thread(target=self.update_timer_label, daemon=True).start()

    def get_idle_time(self):
        try:
            result = subprocess.run(["xprintidle"], stdout=subprocess.PIPE, text=True)
            idle_ms = int(result.stdout.strip())
            return idle_ms / 1000
        except Exception as e:
            print(f"Error getting idle time: {e}")
            return 0

    def update_timer_label(self):
        while True:
            idle_time = self.get_idle_time()
            if idle_time > self.idle_time_threshold and not self.locked:
                self.lock_screen()
            else:
                remaining_time = max(0, self.idle_time_threshold - int(idle_time))
                self.canvas.itemconfigure(self.timer_text, text=f"AUTO🔒{remaining_time}")

                if remaining_time >= 100:
                    self.root.withdraw()
                else:
                    self.root.deiconify()  																						# TODO Change the window styling during the different timings. Configure if you're editing timings

                if remaining_time >= 80:
                    self.canvas.configure(bg="green")
                    self.canvas.itemconfigure(self.timer_text, fill="white")
                elif 40 <= remaining_time < 80:
                    self.canvas.configure(bg="yellow")
                    self.canvas.itemconfigure(self.timer_text, fill="black")
                else:
                    self.canvas.configure(bg="red")
                    self.canvas.itemconfigure(self.timer_text, fill="white")

            time.sleep(1)

    def lock_screen(self):
        os.system("dm-tool lock")
        self.locked = True
        self.canvas.itemconfigure(self.timer_text, text="Locked!")

    def quit(self):
        self.root.quit()

    def run(self):
        """Run the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.mainloop()


if __name__ == "__main__":
    app = IdleTimerApp()
    app.run()


import atexit
atexit.register(remove_lock)