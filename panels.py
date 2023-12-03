from typing import Literal, Tuple
import customtkinter as ctk
from CTkColorPicker import AskColor
from wand.image import text

class Panel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='x', pady=4, ipady=8)

class CheckBoxPanel(Panel):
    def __init__(self, master, name: str):
        super().__init__(master)

        self.value = ctk.BooleanVar()

        ctk.CTkCheckBox(self, text=name, variable=self.value) \
                .pack(expand=True, fill='x', padx=5)

    def get_var(self):
        return self.value

class RealValuePanel(Panel):
    def __init__(self, master, name: str, negative_input: bool):
        super().__init__(master)

        self.can_be_negative = negative_input
        self.value = ctk.StringVar()
        vcmd = self.register(self.validate_real)
        
        ctk.CTkLabel(self, text=name) \
                .pack(expand=True, side='left', fill='x', padx=5)
        ctk.CTkEntry(self, textvariable=self.value, width=100, \
                validate='all', validatecommand=(vcmd, '%P')) \
                .pack(expand=True, side='right', fill='x', padx=5)

    def get_string_var(self):
        return self.value

    def validate_real(self, P):
        if P == '':
            return True
        try:
            val = float(P)
            return True if self.can_be_negative else val >= 0
        except:
            return False

class XYPanel(Panel):
    def __init__(self, master, name: str, negative_input: bool):
        super().__init__(master)

        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=2)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.x_entry = ctk.StringVar()
        self.y_entry = ctk.StringVar()
        vuint = (self.register(self.validate_uint))
        vint = (self.register(self.validate_int))
        vcmd = vint if negative_input else vuint
        
        ctk.CTkLabel(self, text=name, height=20) \
                .grid(row=0, column=0, columnspan=4, padx=5, sticky='ew')

        ctk.CTkLabel(self, text='X:') \
                .grid(row=1, column=0, padx=5, sticky='e')
        ctk.CTkEntry(self, textvariable=self.x_entry, width=50, \
                validate='all', validatecommand=(vcmd, '%P')) \
                .grid(row=1, column=1, padx=5, sticky='w')

        ctk.CTkLabel(self, text='Y:') \
                .grid(row=1, column=2, padx=5, sticky='e')
        ctk.CTkEntry(self, textvariable=self.y_entry, width=50, \
                validate='all', validatecommand=(vcmd, '%P')) \
                .grid(row=1, column=3, padx=5, sticky='w')

    def get_string_vars(self):
        return self.x_entry, self.y_entry
    
    def validate_uint(self, P):
        return str.isdigit(P) or P == ''

    def validate_int(self, P):
        return self.validate_uint(P) or \
                ((P[0] == '-' or P[0] == '+') and self.validate_uint(P[1:]))

class SliderPanel(Panel):
    def __init__(self, master, name: str, type: Literal['float', 'int'], lower_bound, upper_bound):
        super().__init__(master)

        match type:
            case 'float':
                self.is_float = True
                self.value = ctk.DoubleVar()
            case 'int':
                self.is_float = False
                self.value = ctk.IntVar()
        
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.value.trace_add('write', self.format_value)

        ctk.CTkLabel(self, text=name).grid(row=0, column=0, sticky='w', padx=8)
        self.value_label = ctk.CTkLabel(self)
        self.value_label.grid(row=0, column=1, sticky='e', padx=8)
        ctk.CTkSlider(self, variable=self.value, from_=lower_bound, to=upper_bound) \
                .grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)

    def get_number_var(self):
        return self.value
    
    def format_value(self, _a, _b, _c):
        if self.is_float:
            self.value_label.configure(text='{:.3f}'.format(self.value.get()))
        else:
            self.value_label.configure(text=self.value.get())

class ColorPickPanel(Panel):
    def __init__(self, master, name: str):
        super().__init__(master)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.color = ctk.StringVar()
        self.chechbox = ctk.BooleanVar()
        self.last_color = 'None'
        
        ctk.CTkCheckBox(self, text=name, command=self.switch_color_var, variable=self.chechbox) \
                .grid(row=0, column=0, columnspan=4, padx=5, sticky='ew')

        self.button = ctk.CTkButton(self, text='Pick a color', command=self.ask_color, state='disabled') 
        self.button.grid(row=1, column=0, padx=5, sticky='ew')
        self.color_frame = ctk.CTkFrame(self, width=60, height=30)
        self.color_frame.grid(row=1, column=1, padx=5, sticky='ew')

    def get_string_var(self):
        return self.color
    
    def ask_color(self):
        ask_color = AskColor()
        self.color.set(ask_color.get())
        color_value = self.color.get()
        if color_value != 'None':
            self.color_frame.configure(fg_color=self.color.get())

    def switch_color_var(self):
        if self.chechbox.get():
            self.button.configure(state='normal')
            self.color.set(self.last_color)
        else:
            self.button.configure(state='disabled')
            self.last_color = self.color.get()
            self.color.set('None')
   
