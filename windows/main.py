import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
from PIL import Image, ImageTk
import time
import os


class Fenrir:
    def __init__(self, root) -> None:
        """
        Initialize the Fenrir application window.

        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.root.title("Fenrir Editor")

        self.root.overrideredirect(True)
        self.root.geometry("540x90")
        self.root.configure(bg="#19191B")

        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        padding_x = 20
        padding_y = 20

        x = screen_width - window_width - padding_x
        y = screen_height - window_height - padding_y

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.create_custom_toolbar()
        self.create_main_interface()

    def create_main_interface(self):
        """
        Creates the main user interface for the Fenrir application, including buttons for recording, saving, and editing GIFs.
        """
        self.button_frame = tk.Frame(self.root, bg="#19191B")
        self.button_frame.pack(pady=10)

        self.record_time_var = tk.StringVar(value="5s")
        self.time_menu = tk.OptionMenu(
            self.button_frame, self.record_time_var, "5s", "15s", "30s", "60s"
        )
        self.time_menu.grid(row=0, column=0, padx=5)

        self.speed_var = tk.StringVar(value="Medium")
        self.speed_menu = tk.OptionMenu(
            self.button_frame, self.speed_var, "Slow", "Medium", "Fast"
        )
        self.speed_menu.grid(row=0, column=5, padx=5)

        self.time_menu.config(bg="#2E2E2E", fg="#FFFFFF", bd=0)
        self.speed_menu.config(bg="#2E2E2E", fg="#FFFFFF", bd=0)

        self._configure_option_menu(self.time_menu, "#2E2E2E", "#FFFFFF")
        self._configure_option_menu(self.speed_menu, "#2E2E2E", "#FFFFFF")

        menu = self.time_menu["menu"]
        menu.config(bg="#2E2E2E", fg="#FFFFFF", bd=0, relief="flat", font=("Segoe UI", 10))

        menu = self.speed_menu["menu"]
        menu.config(bg="#2E2E2E", fg="#FFFFFF", bd=0, relief="flat", font=("Segoe UI", 10))

        self.time_menu["indicatoron"] = False
        self.speed_menu["indicatoron"] = False

        r_image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "images", "record.png"
        )
        r_icon = Image.open(r_image_path)
        r_icon = r_icon.resize((25, 25))
        self.record_icon = ImageTk.PhotoImage(r_icon)
        self.record_button = tk.Button(
            self.button_frame,
            text="Start Recording",
            command=self.start_selection,
            font=("Segoe UI Semibold", 9, "normal"),
            bg="#19191B",
            fg="#FFFFFF",
            bd=0,
            padx=3,
            pady=3,
            image=self.record_icon,
            compound=tk.LEFT,
        )

        st_image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "images", "stop.png"
        )
        st_icon = Image.open(st_image_path)
        st_icon = st_icon.resize((25, 25))
        self.stop_icon = ImageTk.PhotoImage(st_icon)
        self.stop_record_button = tk.Button(
            self.button_frame,
            text="Stop Recording",
            command=self.stop_recording,
            state="disabled",
            font=("Segoe UI Semibold", 9, "normal"),
            bg="#19191B",
            fg="#FFFFFF",
            bd=0,
            padx=3,
            pady=3,
            image=self.stop_icon,
            compound=tk.LEFT,
        )

        s_image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "images", "save.png"
        )
        s_icon = Image.open(s_image_path)
        s_icon = s_icon.resize((20, 20))
        self.save_icon = ImageTk.PhotoImage(s_icon)
        self.save_button = tk.Button(
            self.button_frame,
            text="Save GIF",
            command=self.save_gif,
            state="disabled",
            font=("Segoe UI Semibold", 9, "normal"),
            bg="#19191B",
            fg="#FFFFFF",
            bd=0,
            padx=3,
            pady=3,
            image=self.save_icon,
            compound=tk.LEFT,
        )

        e_image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "images", "edit.png"
        )
        e_icon = Image.open(e_image_path)
        e_icon = e_icon.resize((20, 20))
        self.edit_icon = ImageTk.PhotoImage(e_icon)
        self.edit_button = tk.Button(
            self.button_frame,
            text="Edit GIF",
            command=self.open_edit_panel,
            state="disabled",
            font=("Segoe UI Semibold", 9, "normal"),
            bg="#19191B",
            fg="#FFFFFF",
            bd=0,
            padx=3,
            pady=3,
            image=self.edit_icon,
            compound=tk.LEFT,
        )

        self.record_button.grid(row=0, column=1, padx=5)
        self.stop_record_button.grid(row=0, column=2, padx=5)
        self.save_button.grid(row=0, column=3, padx=5)
        self.edit_button.grid(row=0, column=4, padx=5)

        self.scroll_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.frames_canvas = tk.Canvas(self.scroll_frame, bg="#2E2E2E")
        self.frames_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frames_container = tk.Frame(self.frames_canvas, bg="#2E2E2E")
        self.frames_canvas.create_window(
            (0, 0), window=self.frames_container, anchor=tk.NW
        )

        self.frames_container.bind("<Configure>", self.update_scrollregion)
        
    def _configure_option_menu(self, option_menu, bg_color, fg_color):
        """
        Configures the dropdown menu of an OptionMenu widget.

        Args:
            option_menu (tk.OptionMenu): The OptionMenu widget to configure.
            bg_color (str): The background color for the dropdown menu.
            fg_color (str): The foreground color (text color) for the dropdown menu.
        """
        menu = option_menu["menu"]
        menu.config(bg=bg_color, fg=fg_color, bd=0, relief="flat")

    def create_custom_toolbar(self):
        """
        Creates a custom toolbar with a title and close button.
        """
        self.toolbar = tk.Frame(self.root, bg="#19191B", height=30)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)

        self.title_label = tk.Label(
            self.toolbar,
            text="Fenrir",
            bg="#19191B",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
        )
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.close_button = tk.Button(
            self.toolbar,
            text="❌",
            command=self.root.destroy,
            bg="#19191B",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
        )
        self.close_button.pack(side=tk.RIGHT)

        self.toolbar.bind("<Button-1>", self.on_drag_start)
        self.toolbar.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        """
        Start dragging the window.

        Args:
            event (tk.Event): The event triggered by clicking the toolbar.
        """
        self.x_start = event.x_root
        self.y_start = event.y_root

    def on_drag_motion(self, event):
        """
        Move the window during dragging.

        Args:
            event (tk.Event): The event triggered by dragging the mouse.
        """
        dx = event.x_root - self.x_start
        dy = event.y_root - self.y_start
        new_x = self.root.winfo_x() + dx
        new_y = self.root.winfo_y() + dy
        self.root.geometry(f"+{new_x}+{new_y}")
        self.x_start = event.x_root
        self.y_start = event.y_root

    def update_scrollregion(self, event):
        """
        Update the scroll region of the canvas.

        Args:
            event (tk.Event): The event triggered by resizing the frames container.
        """
        self.frames_canvas.config(scrollregion=self.frames_canvas.bbox("all"))

    def start_selection(self):
        """
        Start the screen selection process for recording.
        """
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.config(bg="black")

        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        """
        Handle mouse button press event for selection.

        Args:
            event (tk.Event): The event triggered by pressing the mouse button.
        """
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_mouse_drag(self, event):
        """
        Handle mouse drag event for resizing the selection rectangle.

        Args:
            event (tk.Event): The event triggered by dragging the mouse.
        """
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        """
        Handle mouse button release event after selection.

        Args:
            event (tk.Event): The event triggered by releasing the mouse button.
        """
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        start_x, end_x = sorted([self.start_x, end_x])
        start_y, end_y = sorted([self.start_y, end_y])

        self.recording_area = (
            int(start_x),
            int(start_y),
            int(end_x - start_x),
            int(end_y - start_y),
        )

        self.selection_window.destroy()

        self.countdown_label = tk.Label(
            self.root, text="", font=("Helvetica", 48), fg="#FFFFFF", bg="#19191B"
        )
        self.countdown_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.countdown(5)

    def countdown(self, count):
        if count > 0:
            self.countdown_label.config(text=str(count))
            self.root.after(1000, self.countdown, count - 1)
        else:
            self.countdown_label.destroy()
            self.title_label.config(
                text="Recording...",
                bg="#19191B",
                fg="#FFFFFF",
                font=("Segoe UI", 10, "bold"),
            )
            self.root.after(500, self.start_recording)

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.title_label.config(
            text="Fenrir", bg="#19191B", fg="#FFFFFF", font=("Segoe UI", 10, "bold")
        )
        self.record_button.config(state="disabled")
        self.stop_record_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.edit_button.config(state="disabled")
        self.record_screen()

    def stop_recording(self):
        """
        Stop the screen recording.
        """
        self.recording = False
        self.record_button.config(state="normal")
        self.stop_record_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.edit_button.config(state="normal")
        self.countdown_label.destroy()

    def record_screen(self):
        """
        Start the screen recording based on the selected area.
        """
        if not self.recording:
            return
        
        interval = 0.1
        speed = self.speed_var.get()
        if speed == "Slow":
            interval = 0.3
        elif speed == "Medium":
            interval = 0.1
        elif speed == "Fast":
            interval = 0.05

        screen = pyautogui.screenshot(region=self.recording_area)
        self.frames.append(screen)
        time.sleep(interval)

        try:
            record_time = float(self.record_time_var.get().replace("s", ""))
        except ValueError:
            record_time = 5.0

        if len(self.frames) * 0.1 >= record_time:
            self.stop_recording()
            return

        self.record_screen()

    def save_gif(self):
        """
        Save the recorded frames as a GIF file.
        """
        if not self.frames:
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".gif", filetypes=[("GIF files", "*.gif")]
        )
        if save_path:
            self.frames[0].save(
                save_path,
                save_all=True,
                append_images=self.frames[1:],
                loop=0,
                duration=int(100 / 10),
            )
            messagebox.showinfo("Info", f"GIF saved as {save_path}")

    def populate_frame_list(self):
        """
        Populate the frame list with thumbnails and enable editing features.
        """
        for widget in self.frames_container.winfo_children():
            widget.destroy()

        for idx, frame in enumerate(self.frames):
            frame_img = frame.copy()
            frame_img.thumbnail((150, 150))
            frame_photo = ImageTk.PhotoImage(frame_img)

            frame_button = tk.Button(
                self.frames_container,
                image=frame_photo,
                command=lambda idx=idx: self.delete_frame(idx),
            )
            frame_button.image = frame_photo
            frame_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.frames_canvas.update_idletasks()
        self.frames_canvas.config(scrollregion=self.frames_canvas.bbox("all"))

    def display_gif(self):
        """
        Display the GIF and its frames in the editing panel.
        """
        if not self.frames:
            return

        gif_image = ImageTk.PhotoImage(self.frames[0])
        self.edit_gif_label.config(image=gif_image)
        self.edit_gif_label.image = gif_image

        gif_width = gif_image.width()
        gif_height = gif_image.height()

        padding_width = 200
        padding_height = 200

        panel_width = gif_width + padding_width
        panel_height = gif_height + padding_height

        if hasattr(self, "edit_panel") and self.edit_panel.winfo_exists():
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - panel_width) // 2
            y = (screen_height - panel_height) // 2
            self.edit_panel.geometry(f"{panel_width}x{panel_height}+{x}+{y}")

    def open_edit_panel(self):
        """
        Open the GIF editing panel.
        """
        self.edit_panel = tk.Toplevel(self.root)
        self.edit_panel.title("Edit GIF")
        self.edit_panel.overrideredirect(True)

        initial_panel_width = 800
        initial_panel_height = 700

        bg_color = "#19191B"

        gif_width = self.frames[0].width if self.frames else initial_panel_width
        gif_height = self.frames[0].height if self.frames else initial_panel_height

        panel_width = gif_width + 150
        panel_height = gif_height + 150

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - panel_width) // 2
        y = (screen_height - panel_height) // 2

        self.edit_panel.geometry(f"{panel_width}x{panel_height}+{x}+{y}")

        self.edit_panel.configure(bg=bg_color)

        self.edit_gif_label = tk.Label(self.edit_panel, bg="#F2600C")
        self.edit_gif_label.pack(pady=10)

        self.edit_scroll_frame = tk.Frame(self.edit_panel, bd=0, bg=bg_color)
        self.edit_scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.edit_frames_canvas = tk.Canvas(self.edit_scroll_frame, bd=0, bg=bg_color)
        self.edit_frames_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.edit_frames_scrollbar_x = tk.Scrollbar(
            self.edit_scroll_frame,
            orient=tk.HORIZONTAL,
            width=20,
            bg=bg_color,
            command=self.edit_frames_canvas.xview,
        )
        self.edit_frames_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.edit_frames_canvas.config(xscrollcommand=self.edit_frames_scrollbar_x.set)

        self.edit_frames_container = tk.Frame(
            self.edit_frames_canvas, bg=bg_color, bd=0
        )
        self.edit_frames_canvas.create_window(
            (0, 0), window=self.edit_frames_container, anchor=tk.NW
        )

        self.edit_frames_container.bind("<Configure>", self.update_edit_scrollregion)

        self.instruction_label = tk.Label(
            self.edit_scroll_frame,
            text="Click on a frame to delete it.",
            bg=bg_color,
            fg="#FFFFFF",
            font=("Segoe UI", 10),
            padx=5,
            pady=5,
        )
        self.instruction_label.pack(pady=10, padx=10, anchor=tk.W)

        self.close_button = tk.Button(
            self.edit_panel,
            command=self.edit_panel.destroy,
            text="❌",
            bg="#19191B",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
        )
        self.close_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)

        self.populate_edit_frame_list()
        self.display_gif()

    def update_edit_scrollregion(self, event):
        self.edit_frames_canvas.config(scrollregion=self.edit_frames_canvas.bbox("all"))

    def populate_edit_frame_list(self):
        for widget in self.edit_frames_container.winfo_children():
            widget.destroy()

        thumbnail_size = (300, 300)

        for idx, frame in enumerate(self.frames):
            frame_img = frame.copy()
            frame_img.thumbnail(thumbnail_size)
            frame_photo = ImageTk.PhotoImage(frame_img)

            frame_button = tk.Button(
                self.edit_frames_container,
                image=frame_photo,
                command=lambda idx=idx: self.delete_frame(idx),
            )
            frame_button.image = frame_photo
            frame_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_frames_canvas.update_idletasks()
        self.edit_frames_canvas.config(scrollregion=self.edit_frames_canvas.bbox("all"))

    def delete_frame(self, idx):
        """
        Deletes the selected frame from the frames list and updates the frame list in the editing panel.
        """
        if 0 <= idx < len(self.frames):
            del self.frames[idx]
            self.populate_frame_list()
            self.populate_edit_frame_list()


def main():
    root = tk.Tk()
    app = Fenrir(root=root)
    root.mainloop()


if __name__ == "__main__":
    main()
