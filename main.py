from tkinter import filedialog
import customtkinter as ctk
from image_widgets import *
from menu import *
from engine import ENGINE, Parameters, Engine
from math import ceil
from PIL import Image, ImageTk

def fit(child: tuple[int, int], parent: tuple[int, int]):
    parent_aspect_ratio = parent[0] / parent[1]
    child_aspect_ratio = child[0] / child[1]
    if parent_aspect_ratio > child_aspect_ratio:
        return (ceil(parent[1] * child_aspect_ratio).__floor__(), parent[1])
    else:
        return (parent[0], ceil(parent[0] / child_aspect_ratio))

class App(ctk.CTk): 
    def __init__(self) -> None:
        # setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Image Editor')
        self.minsize(800, 500)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # widgets
        self.image_import = ImageImport(self, self.import_image)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # run
        self.after(100, self.check_result_queue)
        self.mainloop()

    def on_closing(self):
        ENGINE.is_running = False
        self.destroy()

    def check_result_queue(self):
        try: 
            new_image_bytes = ENGINE.result_queue.get_nowait()
            self.image.close()
            self.image = Image.open(new_image_bytes)
            self.resize_image(self.last_event)
        except queue.Empty:
            pass
        self.after(100, self.check_result_queue)

    def import_image(self, path):
        if not ENGINE.open_image(path):
            self.image_import.set_error_text("Can't open the file. Please choose another one")
            return

        self.image = Image.open(ENGINE.result_queue.get())
        self.image_tk = ImageTk.PhotoImage(self.image)
        
        self.image_import.grid_forget()
        self.image_import.destroy()
        
        self.menu = Menu(self, self.save_image)
        self.image_frame = ImageFrame(self, self.resize_image, self.close_image)
        self.image_output = self.image_frame.get_canvas()

    def save_image(self):
        filename = filedialog.asksaveasfilename()
        if not ENGINE.save_result(filename):
            pass

    def close_image(self):
        for slave in self.grid_slaves():
            slave.destroy()
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):
        self.last_event = event
        new_size = fit((self.image.width, self.image.height), (event.width, event.height))

        self.image_output.delete('all')
        resized_image = self.image.resize(new_size)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(event.width / 2, event.height / 2, image=self.image_tk)

App()
