import pygame
from pathlib import Path

misc_dir = Path(__file__).parent.parent / "Textures" / "Misc"
ticker = 0

background: pygame.Surface

def initialize(width:int, height:int) -> None:
    global background

    background = pygame.transform.scale(pygame.image.load(misc_dir / "bluescreen.png"), (width, height))

def update(key: int) -> str:
    global ticker
    ticker+= 1
    if ticker > 300 or key == pygame.K_SPACE:
        return "exit"
    return ""

def draw(window: pygame.Surface) -> None:
    window.blit(background, (0,0))