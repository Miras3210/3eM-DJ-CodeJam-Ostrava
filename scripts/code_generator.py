import pygame
from enum import Enum, auto
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))
from dev_mode import Grid, Block, DevPlayer, BlockType, Image_storage


blocks = [
BlockType.No,
BlockType.Death,
BlockType.If,
BlockType.Jump,
BlockType.Minus,
BlockType.Not,
BlockType.Num_0,
BlockType.Num_1,
BlockType.Num_2,
BlockType.Num_3,
BlockType.Num_4,
BlockType.Num_5,
BlockType.Num_6,
BlockType.Num_7,
BlockType.Num_8,
BlockType.Num_9,
BlockType.Plus,
BlockType.Vel,
BlockType.Equal
]

font: pygame.font.Font
grid: Grid = Grid(9, 5, DevPlayer(-1,-1,0,0))
indicator: pygame.Surface
dev_folder = Path(__file__).parent.parent / "Textures" / "Dev"
scale = 4
block_size = 32 * scale

grid.set_block(0,0,BlockType.If)

grid.set_block(1,1,BlockType.If)

selected = BlockType.No

window = pygame.display.set_mode((1600, 900))
width, height = window.get_size()

storage = Image_storage()
def sidebar():
    for i, block in enumerate(blocks):
        window.blit(storage.get_image(block), (((i%3)*128)+1170, (i//3)*128))
        if selected == block:
            pygame.draw.rect(window, (0, 150, 0), (((i%3)*128)+1170, (i//3)*128, 128, 128), 7)

run, clock = True, pygame.time.Clock()
while run:
    window.fill((44,47,63))
    grid.draw(window, 10, 130)
    mx, my = pygame.mouse.get_pos()

    pygame.draw.rect(window, (50,50,50), (1162,0,438,height))
    sidebar()

    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            mx = (mx + 10) // block_size
            my = (my - 130) // block_size
            if 0<= mx < 9 and 0<= my < 5:
                if pygame.mouse.get_pressed()[0]:
                    grid.grid[my][mx].type = selected
                elif pygame.mouse.get_pressed()[2]:
                    grid.grid[my][mx].locked = not grid.grid[my][mx].locked
            mx,my = event.pos
            mx, my = (mx-1170)//128, my//128
            if 0 <= mx <= 3:
                if blocks[3*my + mx] == selected:
                    selected = BlockType.Empty
                else:
                    selected = blocks[3*my + mx]
pygame.quit()