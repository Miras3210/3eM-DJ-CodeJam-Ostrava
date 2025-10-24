import pygame
from enum import Enum, auto
import pathlib

class BlockType(Enum):
    Empty = auto()
    If_statement = auto()

def _img_load_helper(path: pathlib.Path, size: int) -> pygame.surface.Surface:
    return pygame.transform.scale(pygame.image.load(path), (size, size))

class BlockImages:
    def __init__(self, scale: int = 4):
        folder = pathlib.Path(__file__).parent.parent / "Textures"
        self.scale = scale
        self.block_size = 32 * scale
        self.images = {
            BlockType.Empty : _img_load_helper(folder / "dev_block.png", self.block_size),
            BlockType.If_statement : _img_load_helper(folder / "if_block.png", self.block_size),
        }
    def get_image(self, btype: 'BlockType') -> pygame.surface.Surface:
        return self.images.get(btype, self.images[BlockType.If_statement])

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
        for y, line in enumerate(self.grid):
            for x, block in enumerate(line):
                self.imgs.get_image(block.type)
                

class DevPlayer:
    def __init__(self, x:int=0, y:int=0) -> None:
        self.x = x
        self.y = y
        self.direction = Direction.NORMAL

font: pygame.font.Font
txt: pygame.surface.Surface
txt_size: tuple[int,int]
grid: Grid

def initialize(width: int, height: int):
    global font
    font = pygame.font.SysFont("Arial Black", 24)
    global txt, txt_size
    txt = font.render("Dev Mode", 1, (0,0,0))
    txt_size = txt.get_size()
    grid = Grid(15, 10, DevPlayer(0,0))

def draw_game(window: pygame.surface.Surface, width:int, height:int):
    window.fill((44,47,63))
    pygame.draw.rect(window, (0,0,0), (0,0,width*0.1,height))
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