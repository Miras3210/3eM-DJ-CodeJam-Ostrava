import pygame
from enum import Enum, auto
import pathlib

class BlockType(Enum):
    Empty = auto()
    If_statement = auto()

class BlockImages:
    def __init__(self):
        folder = pathlib.Path(__file__).parent.parent / "Textures"
        self.images = {
            BlockType.Empty : pygame.image.load(folder / "dev_block.png"),
            BlockType.If_statement : pygame.image.load(folder / "if_block.png"),
        }
    def get_image(self, btype: 'BlockType'):
        self.images.get(btype, self.images[BlockType.If_statement])

class Direction(Enum):
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    UP = auto()
    NORMAL = auto()

class Block:
    def __init__(self, type: 'BlockType'):
        self.type = type

class Grid:
    def __init__(self, width: int, height: int, player: 'DevPlayer') -> None:
        self.grid = [[Block(BlockType.Empty) for _ in range(width)] for _ in range(height)]
        self.imgs = BlockImages()
    def get_block(self, x:int, y:int) -> 'BlockType':
        return self.grid[y][x].type
    def set_block(self, x: int, y: int, btype: 'BlockType') -> None:
        self.grid[y][x].type = btype
    def delete_block(self, x:int, y: int) -> None:
        self.grid[y][x].type = BlockType.Empty
    def draw(self, surf: pygame.surface.Surface):
        ...

class DevPlayer:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
        self.direction = 1

font: pygame.font.Font
txt: pygame.surface.Surface
txt_size: tuple[int,int]

def initialize(width: int, height: int):
    global font
    font = pygame.font.SysFont("Arial Black", 24)
    global txt, txt_size
    txt = font.render("Dev Mode", 1, (0,0,0))
    txt_size = txt.get_size()

def draw_game(window: pygame.surface.Surface, width:int, height:int):
    window.fill((0,0,0))
    # dev mode indicator
    pygame.draw.rect(window, (150, 150, 150), (0,0,width,txt_size[1]))
    window.blit(txt, (width*0.1 - txt_size[0]//2,0))
    
    

def main(window: pygame.surface.Surface):
    pygame.font.init()
    width, height = window.get_size()
    
    initialize(width, height)
    
    run, clock = True, pygame.time.Clock()
    while run:
        draw_game(window, width, height)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

if __name__ == '__main__':
    window = pygame.display.set_mode((1600,900))
    main(window)
    pygame.quit()