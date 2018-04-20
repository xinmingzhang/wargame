import pygame as pg
from .tools.app import App


def main():
    pg.init()
    game = App()
    from .states.title import Title
    from .states.scenario import Editor
    from .states.help import Help
    from .states.lobby import Lobby
    states = {'title':Title(),'editor':Editor(),'help':Help(),'lobby':Lobby()}
    game.screen_manager.setup_states('title',states)
    game.run()
    pg.quit()