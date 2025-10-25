import pygame
from enum import Enum, auto
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))
from dev_mode import BlockType, Grid, Block

# window = pygame.display.set_mode((width, height))
window = pygame.display.set_mode()
width, height = window.get_size()

run, clock = True, pygame.time.Clock()
while run:
    window.fill((255,255,255))
    
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
pygame.quit()