from engine import *
from panels import RealValuePanel, XYPanel, ColorPickPanel, CheckBoxPanel, SliderPanel
import customtkinter as ctk

class Menu(ctk.CTkTabview):
    def __init__(self, master, save_command):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='nsew', padx=(5, 0))
        SavePanel(master, save_command).grid(row=1, column=0, sticky='nsew', ipady=10, padx=(5, 0), pady=5)

        self.add('Transform')
        self.add('Color')
        self.add('Background')
        self.add('FX')

        self.transform_tab = TransformEditor(self.tab('Transform'))
        self.color_tab = ColorEditor(self.tab('Color'))
        self.background_tab = BackgroundEditor(self.tab('Background'))
        self.fx_tab = FxEditor(self.tab('FX'))

class SavePanel(ctk.CTkFrame):
    def __init__(self, master, save_command):
        super().__init__(master)

        ctk.CTkButton(self, text='Save image', command=save_command).pack(expand=True, fill='both')

class ParamEditor(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def bind_param(self, var: ctk.Variable, object, attr_name: str, var_callback):
        curr = getattr(object, attr_name)
        var.set(str(curr))
        var.trace_add(mode='write', callback=lambda _a, _b, _c: var_callback(var, object, attr_name))

    def bool_var_callback(self, var, object, attr_name):
        ENGINE.set_param(object, attr_name, var.get())
        
    def int_var_callback(self, var, object, attr_name):
        try:
            value = int(var.get())
            ENGINE.set_param(object, attr_name, value)
        except:
            pass

    def float_var_callback(self, var, object, attr_name):
        try:
            value = float(var.get())
            ENGINE.set_param(object, attr_name, value)
        except:
            pass

    def str_var_callback(self, var, object, attr_name):
        if var.get() != '':
            ENGINE.set_param(object, attr_name, var.get())

class TransformEditor(ParamEditor):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')

        pos_x, pos_y = XYPanel(self, 'Position', True).get_string_vars()
        self.bind_param(pos_x, ENGINE.params.transform, 'position_x', self.int_var_callback)
        self.bind_param(pos_y, ENGINE.params.transform, 'position_y', self.int_var_callback)

        size_x, size_y = XYPanel(self, 'Size', False).get_string_vars()
        self.bind_param(size_x, ENGINE.params.transform, 'size_x', self.int_var_callback)
        self.bind_param(size_y, ENGINE.params.transform, 'size_y', self.int_var_callback)

        rotation = RealValuePanel(self, 'Rotation angle', True).get_string_var()
        self.bind_param(rotation, ENGINE.params.transform, 'rotation', self.float_var_callback)

class BackgroundEditor(ParamEditor):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')

        size_x, size_y = XYPanel(self, 'Size', False).get_string_vars()
        self.bind_param(size_x, ENGINE.params.background, 'size_x', self.int_var_callback)
        self.bind_param(size_y, ENGINE.params.background, 'size_y', self.int_var_callback)

        color = ColorPickPanel(self, 'Background color').get_string_var()
        self.bind_param(color, ENGINE.params.background, 'color', self.str_var_callback)

class ColorEditor(ParamEditor):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        
        transparent_color = ColorPickPanel(self, 'Transparent color').get_string_var()
        self.bind_param(transparent_color, ENGINE.params.color, 'transparent_color', self.str_var_callback)
        
        blur = SliderPanel(self, 'Blur', 'float', 0.0, 5.0).get_number_var()
        self.bind_param(blur, ENGINE.params.color, 'blur', self.float_var_callback)

        edge = SliderPanel(self, 'Edge', 'int', 0, 5).get_number_var()
        self.bind_param(edge, ENGINE.params.color, 'edge', self.int_var_callback)

        sharpen = SliderPanel(self, 'Sharpen', 'float', 0.0, 5.0).get_number_var()
        self.bind_param(sharpen, ENGINE.params.color, 'sharpen', self.float_var_callback)

        invert = CheckBoxPanel(self, 'Invert').get_var()
        self.bind_param(invert, ENGINE.params.color, 'invert', self.bool_var_callback)

class FxEditor(ParamEditor):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')

        blue_shift = SliderPanel(self, 'Blue shift', 'float', 1.0, 2.0).get_number_var()
        self.bind_param(blue_shift, ENGINE.params.fx, 'blue_shift', self.float_var_callback)

        colorize = ColorPickPanel(self, 'Colorize').get_string_var()
        self.bind_param(colorize, ENGINE.params.fx, 'colorize', self.str_var_callback)

        sepia = SliderPanel(self, 'Sepia', 'float', 0.0, 1.0).get_number_var()
        self.bind_param(sepia, ENGINE.params.fx, 'sepia', self.float_var_callback)

        swirl = SliderPanel(self, 'Swirl', 'int', 0, 360).get_number_var()
        self.bind_param(swirl, ENGINE.params.fx, 'swirl', self.int_var_callback)

        polaroid = CheckBoxPanel(self, 'Polaroid').get_var()
        self.bind_param(polaroid, ENGINE.params.fx, 'polaroid', self.bool_var_callback)

