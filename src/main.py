from enum import Enum, auto
import pygame

import main_menu
import helper
import dev_mode
import platformer
import bsod

class Scene(Enum):
    MAIN_MENU = auto()
    HELPER = auto()
    GAME = auto()
    DEV = auto()
    BSOD = auto()

def main():
    window = pygame.display.set_mode((1600,900))
    width, height = window.get_size()
    scene = Scene.MAIN_MENU

    main_menu.initialize(width, height)
    helper.initialize(width, height)
    dev_mode.initialize(width, height)
    platformer.initialize(width, height)
    bsod.initialize(width, height)

    key = 0
    run, clock = True, pygame.time.Clock()
    while run:
        match scene:
            case Scene.MAIN_MENU:
                ev = main_menu.update(window)
                if ev == "play":
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    scene = Scene.GAME
                if ev == "help": scene = Scene.HELPER
                if ev == "quit": run = False
                main_menu.draw(window)
            case Scene.HELPER:
                ev = helper.update(window)
                if ev == "exit": scene = Scene.MAIN_MENU
                helper.draw(window)
            case Scene.GAME:
                ev = platformer.update(key, width)
                if ev == "bsod":
                    bsod.ticker = 0
                    scene = Scene.BSOD
                if ev == "switch": scene = Scene.DEV
                platformer.draw(window)
            case Scene.DEV:
                ev = dev_mode.update(key)
                if ev == "switch": scene = Scene.GAME
                dev_mode.draw_game(window)
            case Scene.BSOD:
                ev = bsod.update(key)
                if ev == "exit":
                    platformer.initialize(width, height)
                    dev_mode.initialize(width, height)
                    scene = Scene.GAME
                bsod.draw(window)
        key = 0

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                key = event.key



if __name__ == '__main__':
    main()
    pygame.quit()