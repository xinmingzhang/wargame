import pygame as pg
import copy

def _parse_color(color):

    if color is not None:
        try:
            return pg.Color(str(color))
        except ValueError as e:
            return pg.Color(*color)
    return color


LOADED_FONTS = {}

LABEL_DEFAULTS = {
        "font_path": None,
        "font_size": 12,
        "text_color": "white",
        "fill_color": None,
        "alpha": 255}

class _KwargMixin(object):


    def process_kwargs(self, name, defaults, kwargs):

        settings = copy.deepcopy(defaults)
        for kwarg in kwargs:
            if kwarg in settings:
                if isinstance(kwargs[kwarg], dict):
                    settings[kwarg].update(kwargs[kwarg])
                else:
                    settings[kwarg] = kwargs[kwarg]
            else:
                message = "{} has no keyword: {}"
                raise AttributeError(message.format(name, kwarg))
        for setting in settings:
            setattr(self, setting, settings[setting])

class Label(pg.sprite.Sprite, _KwargMixin):

    def __init__(self, text, rect_attr, *groups, **kwargs):
        super(Label, self).__init__(*groups)
        self.process_kwargs("Label", LABEL_DEFAULTS, kwargs)
        path, size = self.font_path, self.font_size
        if (path, size) not in LOADED_FONTS:
            LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        self.font = LOADED_FONTS[(path, size)]
        self.fill_color = _parse_color(self.fill_color)
        self.text_color = _parse_color(self.text_color)
        self.rect_attr = rect_attr
        self.set_text(text)

        self.original_text = self.text
        self.frequency = 500
        self.timer = 0
        self.visible = True

    def set_text(self, text):
        self.text = text
        self.update_text()

    def update_text(self):
        if self.alpha != 255:
            self.fill_color = pg.Color(*[x + 1 if x < 255 else x - 1 for x in self.text_color[:3]])
        if self.fill_color:
            render_args = (self.text, True, self.text_color, self.fill_color)

        else:
            render_args = (self.text, True, self.text_color)
        self.image = self.font.render(*render_args)
        if self.alpha != 255:
            self.image.set_colorkey(self.fill_color)
            self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(**self.rect_attr)


    def draw(self, surface):
        surface.blit(self.image, self.rect)