import pygame
from enum import Enum, auto
import pathlib

class BlockType(Enum):
    Coin = auto()
    Death = auto()
    Empty = auto()
    Equal = auto()
    Glop = auto()
    If = auto()
    Locked = auto()
    Minus = auto()
    Num_0 = auto()
    Num_1 = auto()
    Num_2 = auto()
    Num_3 = auto()
    Num_4 = auto()
    Num_5 = auto()
    Num_6 = auto()
    Num_7 = auto()
    Num_8 = auto()
    Num_9 = auto()
    Plus = auto()
    Spike = auto()

class PlayerType(Enum):
    Idle = auto()
    Right = auto()
    Left = auto()
    Up = auto()
    Down = auto()

def _img_load_helper(path: pathlib.Path, size: int) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path), (size, size))

class Image_storage:
    def __init__(self, scale: int = 4):
        self.scale = scale
        self.block_size = 32 * scale
        dev_folder = pathlib.Path(__file__).parent.parent / "Textures" / "Dev"
        block_folder = dev_folder / "blocks"
        self.block_images = {
            BlockType.Coin   : _img_load_helper(block_folder / "coin_block.png", self.block_size),
            BlockType.Empty  : _img_load_helper(block_folder / "dev_block.png", self.block_size),
            BlockType.Equal  : _img_load_helper(block_folder / "equal_block.png", self.block_size),
            BlockType.Death  : _img_load_helper(block_folder / "death_block.png", self.block_size),
            BlockType.Glop   : _img_load_helper(block_folder / "glop_block.png", self.block_size),
            BlockType.If     : _img_load_helper(block_folder / "if_block.png", self.block_size),
            BlockType.Locked : _img_load_helper(block_folder / "locked_overlay.png", self.block_size),
            BlockType.Minus  : _img_load_helper(block_folder / "minus_block.png", self.block_size),
            BlockType.Num_0  : _img_load_helper(block_folder / "zero_block.png", self.block_size),
            BlockType.Num_1  : _img_load_helper(block_folder / "one_block.png", self.block_size),
            BlockType.Num_2  : _img_load_helper(block_folder / "two_block.png", self.block_size),
            BlockType.Num_3  : _img_load_helper(block_folder / "three_block.png", self.block_size),
            BlockType.Num_4  : _img_load_helper(block_folder / "four_block.png", self.block_size),
            BlockType.Num_5  : _img_load_helper(block_folder / "five_block.png", self.block_size),
            BlockType.Num_6  : _img_load_helper(block_folder / "six_block.png", self.block_size),
            BlockType.Num_7  : _img_load_helper(block_folder / "seven_block.png", self.block_size),
            BlockType.Num_8  : _img_load_helper(block_folder / "eight_block.png", self.block_size),
            BlockType.Num_9  : _img_load_helper(block_folder / "nine_block.png", self.block_size),
            BlockType.Plus   : _img_load_helper(block_folder / "plus_block.png", self.block_size),
            BlockType.Spike  : _img_load_helper(block_folder / "spike_block.png", self.block_size),
        }
        player_folder = dev_folder / "characters"
        self.player_images = {
            PlayerType.Idle  : _img_load_helper(player_folder / "nurd.png", self.block_size),
            PlayerType.Right : _img_load_helper(player_folder / "nurd_right.png", self.block_size),
            PlayerType.Left  : _img_load_helper(player_folder / "nurd_left.png", self.block_size),
            PlayerType.Up    : _img_load_helper(player_folder / "nurd_up.png", self.block_size),
            PlayerType.Down  : _img_load_helper(player_folder / "nurd_down.png", self.block_size),
        }

    def get_image(self, btype: 'BlockType') -> pygame.Surface:
        return self.block_images.get(btype, self.block_images[BlockType.If])

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
        self.width, self.height = width, height
        self.grid = [[Block(BlockType.Empty) for _ in range(width)] for _ in range(height)]
        self.imgs = Image_storage()
    def get_block(self, x:int, y:int) -> 'BlockType':
        return self.grid[y][x].type
    def set_block(self, x: int, y: int, btype: 'BlockType') -> None:
        self.grid[y][x].type = btype
    def delete_block(self, x:int, y: int) -> None:
        self.grid[y][x].type = BlockType.Empty
    def draw(self, display: pygame.Surface, offset_x: int=0, offset_y: int=0,
             scroll_x: int = 0, scroll_y: int = 0, max_x: int = 0, max_y: int = 0):
        tile = self.imgs.block_size

        vis_w = max_x if max_x else self.width * tile - scroll_x
        vis_h = max_y if max_y else self.height * tile - scroll_y

        nsurf = pygame.Surface((max_x if max_x else self.width * tile - scroll_x,
                                max_y if max_y else self.height * tile - scroll_y),
                               pygame.SRCALPHA)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                img = self.imgs.get_image(self.grid[y][x].type)
                draw_x = x * tile - scroll_x
                draw_y = y * tile - scroll_y
                nsurf.blit(img, (draw_x, draw_y))

        # Draw the clipped result onto the main display
        display.blit(nsurf, (offset_x, offset_y))

class DevPlayer:
    def __init__(self, x:int=0, y:int=0) -> None:
        self.x = x
        self.y = y
        self.direction = Direction.NORMAL

font: pygame.font.Font
txt: pygame.Surface
txt_size: tuple[int,int]
grid: Grid

def initialize(width: int, height: int):
    global font
    font = pygame.font.SysFont("Arial Black", 24)
    global txt, txt_size
    txt = font.render("Dev Mode", 1, (0,0,0))
    txt_size = txt.get_size()

    global grid
    grid = Grid(0,0, DevPlayer(0,0))
    grid.set_block(1,1,BlockType.If)
    grid.set_block(2,1,BlockType.Glop)
    grid.set_block(2,2,BlockType.Death)

def draw_game(window: pygame.Surface, width:int, height:int):
    window.fill((44,47,63))
    pygame.draw.rect(window, (0,0,0), (0,0,width*0.05,height))
    # dev mode indicator
    pygame.draw.rect(window, (150, 150, 150), (0,0,width,txt_size[1]))
    window.blit(txt, (width*0.1 - txt_size[0]//2,0))
    # draw grid
    grid.draw(window, int(width*0.05), txt_size[1], 0, 0)

def main(window: pygame.Surface):
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