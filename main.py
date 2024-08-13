import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from tkinter import ttk
import pyautogui
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time

class Fenrir:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Fenrir Editor")

        self.root.overrideredirect(True)
        self.root.geometry("400x50")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.record_time_var = tk.IntVar(value=5)
        self.time_menu = tk.OptionMenu(self.button_frame, self.record_time_var, 5, 15, 30, 60)
        self.time_menu.grid(row=0, column=0, padx=5)

        self.record_button = tk.Button(self.button_frame, text="Start Recording", command=self.start_selection)
        self.stop_record_button = tk.Button(self.button_frame, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.save_button = tk.Button(self.button_frame, text="Save GIF", command=self.save_gif, state="disabled")
        self.edit_button = tk.Button(self.button_frame, text="Edit GIF", command=self.open_edit_panel, state="disabled")

        self.record_button.grid(row=0, column=1, padx=5)
        self.stop_record_button.grid(row=0, column=2, padx=5)
        self.save_button.grid(row=0, column=3, padx=5)
        self.edit_button.grid(row=0, column=4, padx=5)

        self.scroll_frame = tk.Frame(root)
        self.scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.frames_canvas = tk.Canvas(self.scroll_frame)
        self.frames_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frames_container = tk.Frame(self.frames_canvas)
        self.frames_canvas.create_window((0, 0), window=self.frames_container, anchor=tk.NW)

        self.frames_container.bind("<Configure>", self.update_scrollregion)

        self.frames = []
        self.recording = False
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.gif_image = None
        self.speed_var = tk.DoubleVar(value=1.0)

        self.create_rounded_window()

    def create_rounded_window(self):
        self.canvas = tk.Canvas(self.root, width=400, height=50, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_oval(0, 0, 20, 20, fill='black', outline='black')
        self.canvas.create_oval(380, 0, 400, 20, fill='black', outline='black')
        self.canvas.create_oval(0, 30, 20, 50, fill='black', outline='black')
        self.canvas.create_oval(380, 30, 400, 50, fill='black', outline='black')

        self.canvas.create_rectangle(20, 0, 380, 30, fill='black', outline='black')

        self.close_button = tk.Button(self.canvas, text='X', command=self.root.destroy, bg='black', fg='white', bd=0, relief='flat')
        self.close_button.place(x=370, y=0)

    def update_scrollregion(self, event):
        self.frames_canvas.config(scrollregion=self.frames_canvas.bbox("all"))

    def start_selection(self):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.config(bg='black')

        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.recording_area = (int(self.start_x), int(self.start_y), int(end_x - self.start_x), int(end_y - self.start_y))
        self.selection_window.destroy()

        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 48), fg="black")
        self.countdown_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.countdown(5)

    def countdown(self, count):
        if count > 0:
            self.countdown_label.config(text=str(count))
            self.root.after(1000, self.countdown, count - 1)
        else:
            self.countdown_label.config(text="Recording...", fg="green")
            self.root.after(500, self.start_recording)

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.record_button.config(state="disabled")
        self.stop_record_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.record_screen()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(state="normal")
        self.stop_record_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.edit_button.config(state="normal")
        self.countdown_label.destroy()

    def record_screen(self):
        if not self.recording:
            return
        
        screen = pyautogui.screenshot(region=self.recording_area)
        self.frames.append(screen)
        time.sleep(0.1)

        if len(self.frames) * 0.1 >= self.record_time_var.get():
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
                append_images=self.frames[1:],
                loop=0,
                duration=int(100 / self.speed_var.get())
            )
            messagebox.showinfo("Info", f"GIF saved as {save_path}")

    def populate_frame_list(self):
        for widget in self.frames_container.winfo_children():
            widget.destroy()

        for idx, frame in enumerate(self.frames):
            frame_img = frame.copy()
            frame_img.thumbnail((100, 100))
            frame_photo = ImageTk.PhotoImage(frame_img)

            frame_button = tk.Button(self.frames_container, image=frame_photo, command=lambda idx=idx: self.delete_frame(idx))
            frame_button.image = frame_photo
            frame_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.speed_menu = tk.OptionMenu(self.frames_container, self.speed_var, 0.5, 1.0, 1.5, 2.0)
        self.speed_menu.pack(pady=5)

        self.frames_canvas.update_idletasks()
        self.frames_canvas.config(scrollregion=self.frames_canvas.bbox("all"))

    def display_gif(self):
        if self.frames:
            gif_image = self.frames[0].copy()
            self.gif_image = ImageTk.PhotoImage(gif_image)
            self.gif_label.config(image=self.gif_image)
        
            if hasattr(self, 'edit_panel') and self.edit_panel:
                edit_gif_image = self.frames[0].copy()
                self.edit_gif_image = ImageTk.PhotoImage(edit_gif_image)
                self.edit_gif_label.config(image=self.edit_gif_image)

    def open_edit_panel(self):
        self.edit_panel = tk.Toplevel(self.root)
        self.edit_panel.title("Edit GIF")
        self.edit_panel.geometry("800x600")

        self.edit_gif_label = tk.Label(self.edit_panel)
        self.edit_gif_label.pack(pady=10)

        self.edit_scroll_frame = tk.Frame(self.edit_panel)
        self.edit_scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.edit_frames_canvas = tk.Canvas(self.edit_scroll_frame)
        self.edit_frames_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.edit_frames_scrollbar_x = tk.Scrollbar(self.edit_scroll_frame, orient=tk.HORIZONTAL, width=60, command=self.edit_frames_canvas.xview)
        self.edit_frames_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.edit_frames_canvas.config(xscrollcommand=self.edit_frames_scrollbar_x.set)

        self.edit_frames_container = tk.Frame(self.edit_frames_canvas)
        self.edit_frames_canvas.create_window((0, 0), window=self.edit_frames_container, anchor=tk.NW)

        self.edit_frames_container.bind("<Configure>", self.update_edit_scrollregion)

        self.close_button = tk.Button(self.edit_panel, text="Close", command=self.edit_panel.destroy)
        self.close_button.pack(pady=10)

        self.populate_edit_frame_list()
        self.display_gif()  

    def update_edit_scrollregion(self, event):
        self.edit_frames_canvas.config(scrollregion=self.edit_frames_canvas.bbox("all"))

    def populate_edit_frame_list(self):
        for widget in self.edit_frames_container.winfo_children():
            widget.destroy()

        for idx, frame in enumerate(self.frames):
            frame_img = frame.copy()
            frame_img.thumbnail((100, 100))
            frame_photo = ImageTk.PhotoImage(frame_img)

            frame_button = tk.Button(self.edit_frames_container, image=frame_photo, command=lambda idx=idx: self.delete_frame(idx))
            frame_button.image = frame_photo
            frame_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_speed_menu = tk.OptionMenu(self.edit_frames_container, self.speed_var, 0.5, 1.0, 1.5, 2.0)
        self.edit_speed_menu.pack(pady=5)

        self.edit_frames_canvas.update_idletasks()
        self.edit_frames_canvas.config(scrollregion=self.edit_frames_canvas.bbox("all"))

    def delete_frame(self, idx):
        if 0 <= idx < len(self.frames):
            del self.frames[idx]
            self.populate_frame_list()  
            self.populate_edit_frame_list()  
if __name__ == "__main__":
    root = tk.Tk()
    app = Fenrir(root=root)
    root.mainloop()
