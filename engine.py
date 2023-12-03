from io import BytesIO
import threading
from typing import Tuple
import time
import queue
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

class Parameters:
    def __init__(self, bg_size: Tuple[int, int], img_size: Tuple[int, int]):
        self.background = BackgroundParams(bg_size)
        self.transform = TransformParams(img_size)
        self.color = ColorParams()
        self.fx = FxParams()

class BackgroundParams():
    def __init__(self, size: Tuple[int, int]):
        self.size_x = size[0]
        self.size_y = size[1]
        self.color = 'None'

class TransformParams():
    def __init__(self, size: Tuple[int, int]):
        self.position_x = 0
        self.position_y = 0
        self.rotation = 0.0
        self.size_x = size[0]
        self.size_y = size[1]

class ColorParams():
    def __init__(self):
        self.transparent_color = 'None'
        self.blur = 0.0
        self.edge = 0
        self.sharpen = 0.0
        self.invert = False

class FxParams():
    def __init__(self):
        self.blue_shift = 1.0
        self.colorize = 'None'
        self.sepia = 0.0
        self.swirl = 0
        self.polaroid = False

class Engine:
    def __init__(self) -> None:
        self.changed = False
        self.bg_changed = False
        self.is_running = True
        self.result_queue = queue.Queue()

    def open_image(self, path: str) -> bool:
        try:
            self.image = Image(filename=path)
        except:
            print("Can't open the file. Please choose another one.")
            return False
        self.params = Parameters(bg_size=self.image.size, img_size=self.image.size)
        self.changed = True
        self.bg_changed = True
        return True

    def create_default_bg(self) -> None:
        bg = self.params.background
        color = self.params.background.color
        self.bg = Image(width=bg.size_x, height=bg.size_y, background=Color(color), format='png')

    def composite(self) -> None:
        with Drawing() as draw:
            tr = self.params.transform
            
            self.image_mut.rotate(tr.rotation)
            width, height = self.image_mut.width, self.image_mut.height
            
            self.result = self.bg.clone()
            self.result.format = 'png'
            draw.composite(operator='over', left=tr.position_x, top=tr.position_y, 
                           width=width, height=height, image=self.image_mut)
            draw(self.result)

    def apply_effects(self) -> None:
        clr = self.params.color
        if clr.transparent_color != 'None':
            self.image_mut.transparent_color(clr.transparent_color, 0.0, fuzz=0)
        if clr.blur != 0:
            self.image_mut.gaussian_blur(sigma=clr.blur)
        if clr.edge != 0:
            self.image_mut.edge(clr.edge)
        if clr.sharpen != 0:
            self.image_mut.sharpen(sigma=clr.sharpen)
        if clr.invert:
            self.image_mut.negate()

    def apply_fx(self) -> None:
        fx = self.params.fx
        if fx.blue_shift != 1.0:
            self.image_mut.blue_shift(fx.blue_shift)
        if fx.colorize != 'None':
            print(fx.colorize)
            self.image_mut.colorize(fx.colorize, alpha='rgb(50%, 50%, 50%)')
        if fx.sepia != 0:
            self.image_mut.sepia_tone(fx.sepia)
        if fx.swirl != 0:
            self.image_mut.swirl(fx.swirl)
        if fx.polaroid:
            self.image_mut.polaroid()

    def apply_all(self) -> None:
        if self.bg_changed:
            self.bg_changed = False
            self.create_default_bg()
        
        tr = self.params.transform
        self.image_mut = self.image.clone()
        self.image_mut.format = 'png'
        self.image_mut.resize(tr.size_x, tr.size_y)
        self.apply_effects()
        self.apply_fx()
        self.composite()
        #self.bg.save(filename='tmp/display.jpg')

    def get_image_bytes(self) -> BytesIO:
        return BytesIO(self.result.make_blob())

    def save_result(self, filename: str) -> None:
        self.result.save(filename=filename)

    def set_param(self, obj, param_name, value):
        if param_name[0:4] == 'size' and value <= 0:
            return
        setattr(obj, param_name, value)
        self.changed = True
        if obj == self.params.background:
            self.bg_changed = True

    def start(self):
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def run(self):
        while self.is_running:
            time.sleep(0.05)
            if self.changed:
                self.changed = False
                self.apply_all()
                self.result_queue.put(self.get_image_bytes())
                

ENGINE = Engine()
ENGINE.start()
