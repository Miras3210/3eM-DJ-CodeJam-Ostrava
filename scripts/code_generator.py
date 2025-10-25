import pygame
from enum import Enum, auto
import pathlib

class BlockType(Enum):
    No = auto()
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
    Selected = auto()

def _img_load_helper(path: pathlib.Path, size: int) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path), (size, size))

dev_folder = pathlib.Path(__file__).parent.parent / "Textures" / "Dev"
scale = 4
block_size = 32 * scale
class Image_storage:
    def __init__(self):
        block_folder = dev_folder / "blocks"
        self.block_images = {
            BlockType.Coin   : _img_load_helper(block_folder / "coin_block.png", block_size),
            BlockType.Empty  : _img_load_helper(block_folder / "dev_block.png", block_size),
            BlockType.Equal  : _img_load_helper(block_folder / "equal_block.png", block_size),
            BlockType.Death  : _img_load_helper(block_folder / "death_block.png", block_size),
            BlockType.Glop   : _img_load_helper(block_folder / "glop_block.png", block_size),
            BlockType.If     : _img_load_helper(block_folder / "if_block.png", block_size),
            BlockType.Locked : _img_load_helper(block_folder / "locked_overlay.png", block_size),
            BlockType.Minus  : _img_load_helper(block_folder / "minus_block.png", block_size),
            BlockType.Num_0  : _img_load_helper(block_folder / "zero_block.png", block_size),
            BlockType.Num_1  : _img_load_helper(block_folder / "one_block.png", block_size),
            BlockType.Num_2  : _img_load_helper(block_folder / "two_block.png", block_size),
            BlockType.Num_3  : _img_load_helper(block_folder / "three_block.png", block_size),
            BlockType.Num_4  : _img_load_helper(block_folder / "four_block.png", block_size),
            BlockType.Num_5  : _img_load_helper(block_folder / "five_block.png", block_size),
            BlockType.Num_6  : _img_load_helper(block_folder / "six_block.png", block_size),
            BlockType.Num_7  : _img_load_helper(block_folder / "seven_block.png", block_size),
            BlockType.Num_8  : _img_load_helper(block_folder / "eight_block.png", block_size),
            BlockType.Num_9  : _img_load_helper(block_folder / "nine_block.png", block_size),
            BlockType.Plus   : _img_load_helper(block_folder / "plus_block.png", block_size),
            BlockType.Spike  : _img_load_helper(block_folder / "spike_block.png", block_size),
            BlockType.Selected:_img_load_helper(block_folder / "selected_overlay.png", block_size),
        }

    def get_image(self, btype: 'BlockType') -> pygame.Surface:
        return self.block_images.get(btype, self.block_images[BlockType.Empty])

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