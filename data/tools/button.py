import pygame as pg
import copy

LOADED_FONTS = {}

#Default values for Button objects - see Button class for specifics
BUTTON_DEFAULTS = {
        "button_size": (128, 32),
        "call": None,
        "args": None,
        "call_on_up": True,
        "font": None,
        "font_size": 36,
        "text": None,
        "hover_text": None,
        "disable_text": None,
        "text_color": pg.Color("white"),
        "hover_text_color": None,
        "disable_text_color": None,
        "fill_color": None,
        "hover_fill_color": None,
        "disable_fill_color": None,
        "idle_image": None,
        "hover_image": None,
        "disable_image": None,
        "hover_sound": None,
        "click_sound": None,
        "visible": True,
        "active": True,
        "bindings": ()}

def _parse_color(color):

    if color is not None:
        try:
            return pg.Color(str(color))
        except ValueError as e:
            return pg.Color(*color)
    return color

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

class ButtonGroup(pg.sprite.Group):
    """
    A sprite Group modified to allow calling each sprite in the group's
    get_event method similar to using Group.update to call each sprite's
    update method.
    """
    def get_event(self, event, *args, **kwargs):
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)


class Button(pg.sprite.Sprite, _KwargMixin):
    """
    A clickable button which accepts a number of keyword
    arguments to allow customization of a button's
    appearance and behavior.
    """
    _invisible = pg.Surface((1,1)).convert_alpha()
    _invisible.fill((0,0,0,0))

    def __init__(self, topleft, *groups, **kwargs):
        """
        Instantiate a Button object based on the keyword arguments. Buttons
        have three possible states (idle, hovered and disabled) and appearance
        options for each state. The button is idle when the mouse is not over
        the button and hovered when it is. The button is disabled when
        Button.active is False and will not respond to events.
        USAGE
        For buttons to function properly, Button.update must be called
        each frame/tick/update with the current mouse position and
        Button.get_event must be called for each event in the event queue.
        ARGS
        topleft: the topleft screen position of the button
        KWARGS
        Buttons accept a number of keyword arguments that may be
        passed individually, as a dict of "keyword": value pairs or a combination
        of the two. Any args that are not passed to __init__ will use the default
        values stored in the BUTTON_DEAFULTS dict
        "button_size": the size of the button in pixels
        "call": callback function
        "args": args to be passed to callback function
        "call_on_up": set to True for clicks to occur on mouseup/keyup
                             set to False for clicks to occur on mousedown/keydown
        "font": path to font - uses pygame's default if None
        "font_size": font size in pixels
        "text": text to be displayed when button is idle
        "hover_text": text to be displayed when mouse is over button
        "disable_text": text to be displayed when button is disabled
        "text_color": text color when button is idle
        "hover_text_color": text_color when mouse is hovering over button
        "disable_text_color": text color when button is disabled (self.active == False)
        "fill_color": button color when button is idle, transparent if None
        "hover_fill_color": button color when hovered, transparent if None
        "disable_fill_color": button color when disabled, transparent if None
        "idle_image": button image when idle, ignored if None
        "hover_image": button image when hovered, ignored if None
        "disable_image": button image when disabled, ignored if None
        "hover_sound": Sound object to play when hovered, ignored if None
        "click_sound": Sound object to play when button is clicked, ignored if None
        "visible": whether the button should be drawn to the screen
        "active": whether the button should respond to events
        "bindings": which buttons, if any, should be able to click the button - values should
                         be a sequence of pygame key constants, e.g, (pg.K_UP, pg.K_w)
        """
        super(Button, self).__init__(*groups)
        color_args = ("text_color", "hover_text_color", "disable_text_color",
                           "fill_color", "hover_fill_color", "disable_fill_color")
        for c_arg in color_args:
            if c_arg in kwargs and kwargs[c_arg] is not None:
                 kwargs[c_arg] = _parse_color(kwargs[c_arg])
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(topleft, self.button_size)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        """Render text for each button state."""
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text": text, "hover": hover, "disable": disable}

    def make_image(self, fill, image, text):
        """Create needed button images."""
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        """Process events."""
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        """Process mouseup and keyup events."""
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        """Process mousedown and keydown events."""
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:

                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        """
        Determine whehter the mouse is over the button and
        change button appearance if necessary. Calling
        ButtonGroup.update will call update on any Buttons
        in the group.
        """
        hover = self.rect.collidepoint(prescaled_mouse_pos)
        pressed = pg.key.get_pressed()
        if any(pressed[key] for key in self.bindings):
            hover = True
        if not self.visible:
            self.image = Button._invisible
        elif self.active:
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        """Draw the button to the screen."""
        surface.blit(self.image, self.rect)
