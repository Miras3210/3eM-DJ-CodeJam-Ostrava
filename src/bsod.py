import pygame
from pathlib import Path
from location_helper import project_root

misc_dir = project_root() / "Textures" / "Misc"
ticker = 0

background: pygame.Surface

def initialize(width:int, height:int) -> None:
    global background

    background = pygame.transform.scale(pygame.image.load(misc_dir / "bluescreen_unknown.png"), (width, height))

def update(key: int) -> str:
    global ticker
    ticker+= 1
    if ticker > 300 or key:
        return "exit"
    return ""

def draw(window: pygame.Surface) -> None:
    window.blit(background, (0,0))