import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
from PIL import Image
import time

class Fenrir:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Fenrir Editor")
        self.root.geometry("500x450")

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_record_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_record_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Button", command=self.save_gif, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.frames = []
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.record_button.config(tk.DISABLED)
        self.stop_record_button.config(tk.NORMAL)
        self.save_button.config(tk.DISABLED)
        self.record_screen()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(tk.NORMAL)
        self.stop_record_button.config(tk.DISABLED)
        self.save_button.config(tk.NORMAL)

    def record_screen(self):
        if not self.recording:
            return
        
        screen = pyautogui.screenshot()
        self.frames.append(screen)
        time.sleep(0.1)

        if len(self.frames) * 0.1 >= 5:
            self.stop_recording()
            return
        
        self.record_screen()
    
    def save_gif(self):
        if not self.frames:
            return
        
        save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
        if save_path:
            self.frames[0].save(
                save_path,
                save_all=True,
                append_images =self.frames[1:],
                loop=0,
                duration=100
            )
            messagebox.showinfo("Info", f"GIF saved as {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Fenrir(root=root)
    root.mainloop()