import customtkinter as ctk
from tkinter import filedialog

class ImageImport(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.grid(column=0, columnspan=2, row=0, sticky = 'nsew')
        self.callback = callback

        ctk.CTkButton(self, text='Open image', command=self.open_dialogue).pack(expand=True)
        self.error_label = ctk.CTkLabel(self, text='', text_color='red', fg_color='transparent')
        self.error_label.pack(side='bottom')

    def open_dialogue(self):
        file = filedialog.askopenfile()
        if file != None:
            path = file.name
            file.close()
            self.callback(path)

    def set_error_text(self, text):
        self.error_label.configure(text=text)

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master, resize_callback, close_callback):
        super().__init__(master)
        self.grid(row=0, rowspan=2, column=1, sticky='nsew', padx=5, pady=5)

        CloseButtonFrame(self, close_callback).pack(side='top', fill='x')
        self.canvas = ImageOutput(self, resize_callback)
        self.canvas.pack(expand=True, side='bottom', fill='both')

    def get_canvas(self):
        return self.canvas

class CloseButtonFrame(ctk.CTkFrame):
    def __init__(self, master, close_callback):
        super().__init__(master)
        
        ctk.CTkButton(self, text='X', command=close_callback, width=20, \
                fg_color='transparent', anchor='e', border_spacing=0) \
                .pack(side='right', fill='y')

class ImageOutput(ctk.CTkCanvas):
    def __init__(self, master, resize_callback):
        super().__init__(master, bd=0, highlightthickness=0, relief='ridge', bg='#262626')
        self.bind('<Configure>', resize_callback)


