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

class PlayerDir(Enum):
    Idle = auto()
    Right = auto()
    Left = auto()
    Up = auto()
    Down = auto()

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

class Block:
    def __init__(self, type: 'BlockType'):
        self.type = type
        self.locked = False

class Grid:
    def __init__(self, width: int, height: int, player: 'DevPlayer') -> None:
        self.width, self.height = width, height
        self.grid = [[Block(BlockType.Empty) for _ in range(width)] for _ in range(height)]
        self.imgs = Image_storage()
        self.player = player
    def get_block(self, x:int, y:int) -> 'BlockType':
        return self.grid[y][x].type
    def set_block(self, x: int, y: int, btype: 'BlockType') -> None:
        self.grid[y][x].type = btype
    def lock_block(self, x: int, y: int) -> None:
        self.grid[y][x].locked = True
    def unlock_block(self, x: int, y: int) -> None:
        self.grid[y][x].locked = False

    def delete_block(self, x:int, y: int) -> None:
        self.grid[y][x].type = BlockType.Empty
    def draw(self, display: pygame.Surface, offset_x: int=0, offset_y: int=0,
             scroll_x: int = 0, scroll_y: int = 0, max_x: int = 0, max_y: int = 0):
        nsurf = pygame.Surface((max_x if max_x else self.width * block_size - scroll_x,
                                max_y if max_y else self.height * block_size - scroll_y),
                               pygame.SRCALPHA)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                img = self.imgs.get_image(self.grid[y][x].type)
                nsurf.blit(img, (x * block_size - scroll_x, y * block_size - scroll_y))
                if self.grid[y][x].locked:
                    nsurf.blit(self.imgs.get_image(BlockType.Locked), (x * block_size - scroll_x, y * block_size - scroll_y))
                # if (x,y) == (self.player.x, self.player.y):
        pl = self.player
        nsurf.blit(pl.get_image(), (pl.x * block_size - scroll_x, pl.y * block_size - scroll_y))
        if pl.selected:
            nsurf.blit(self.imgs.block_images[BlockType.Selected],
                   (-scroll_x + block_size * (pl.x + pl.selected_rel_pos(0,0)[0]),
                    -scroll_y + block_size * (pl.y + pl.selected_rel_pos(0,0)[1])))

        # Draw the clipped result onto the main display
        display.blit(nsurf, (offset_x, offset_y))

class DevPlayer:
    def __init__(self, x:int, y:int, w:int, h:int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tick = 0
        self.grid: 'Grid'
        self.select_dir = PlayerDir.Right
        self.selected = False
        self.direction = PlayerDir.Idle
        player_folder = dev_folder / "characters"
        self.player_images = {
            PlayerDir.Idle  : _img_load_helper(player_folder / "nurd.png", block_size),
            PlayerDir.Right : _img_load_helper(player_folder / "nurd_right.png", block_size),
            PlayerDir.Left  : _img_load_helper(player_folder / "nurd_left.png", block_size),
            PlayerDir.Up    : _img_load_helper(player_folder / "nurd_up.png", block_size),
            PlayerDir.Down  : _img_load_helper(player_folder / "nurd_down.png", block_size),
        }
    def get_image(self) -> pygame.Surface:
        return self.player_images.get(self.direction, self.player_images[PlayerDir.Idle])

    def grid_block(self, x:int, y:int) -> 'BlockType':
        if 0 <= self.y+y < self.h and 0 <= self.x+x < self.w:
            if self.grid.grid[self.y+y][self.x+x].locked:
                return BlockType.No
            return self.grid.grid[self.y+y][self.x+x].type
        return BlockType.No

    def swap_grid_block(self, x:int,y:int,x2:int,y2:int):
        self.grid.grid[y][x], self.grid.grid[y2][x2] = self.grid.grid[y2][x2], self.grid.grid[y][x]

    def selected_rel_pos(self,x: int, y: int, add_self:bool = False) -> tuple[int,int]:
        if self.select_dir == PlayerDir.Up: y-= 1
        if self.select_dir == PlayerDir.Down: y+= 1
        if self.select_dir == PlayerDir.Left: x-= 1
        if self.select_dir == PlayerDir.Right: x+= 1
        if add_self:
            return (x + self.x, y + self.y)
        return (x, y)
    
    def move(self, direction: 'PlayerDir') -> None:
        match direction:
            case PlayerDir.Right:
                if self.selected and self.select_dir != PlayerDir.Right:
                    if self.grid_block(1,0) == BlockType.Empty and self.grid_block(*self.selected_rel_pos(1,0)) == BlockType.Empty:
                        self.swap_grid_block(*self.selected_rel_pos(0,0,True), *self.selected_rel_pos(1,0,True))
                        self.x+= 1
                else:
                    if self.grid_block(1,0) == BlockType.Empty:
                        self.x+= 1
                    elif self.grid_block(2,0) == BlockType.Empty and self.grid_block(1,0) != BlockType.No:
                        self.x+= 1
                        self.swap_grid_block(self.x, self.y, self.x+1, self.y)
                    self.direction = PlayerDir.Right
                    self.select_dir = PlayerDir.Right
            case PlayerDir.Left:
                if self.selected and self.select_dir != PlayerDir.Left:
                    if self.grid_block(-1,0) == BlockType.Empty and self.grid_block(*self.selected_rel_pos(-1,0)) == BlockType.Empty:
                        self.swap_grid_block(*self.selected_rel_pos(0,0,True), *self.selected_rel_pos(-1,0,True))
                        self.x-= 1
                else:
                    if self.grid_block(-1,0) == BlockType.Empty:
                        self.x-= 1
                    elif self.grid_block(-2,0) == BlockType.Empty and self.grid_block(-1,0) != BlockType.No:
                        self.x-= 1
                        self.swap_grid_block(self.x, self.y, self.x-1, self.y)
                    self.direction = PlayerDir.Left
                    self.select_dir = PlayerDir.Left
            case PlayerDir.Up:
                if self.selected and self.select_dir != PlayerDir.Up:
                    if self.grid_block(0,-1) == BlockType.Empty and self.grid_block(*self.selected_rel_pos(0,-1)) == BlockType.Empty:
                        self.swap_grid_block(*self.selected_rel_pos(0,0,True), *self.selected_rel_pos(0,-1,True))
                        self.y-= 1
                else:
                    if self.grid_block(0,-1) == BlockType.Empty:
                        self.y-= 1
                    elif self.grid_block(0,-2) == BlockType.Empty and self.grid_block(0,-1) != BlockType.No:
                        self.y-= 1
                        self.swap_grid_block(self.x, self.y, self.x, self.y-1)
                    self.direction = PlayerDir.Up
                    self.select_dir = PlayerDir.Up
            case PlayerDir.Down:
                if self.selected and self.select_dir != PlayerDir.Down:
                    if self.grid_block(0,1) == BlockType.Empty and self.grid_block(*self.selected_rel_pos(0,1)) == BlockType.Empty:
                        self.swap_grid_block(*self.selected_rel_pos(0,0,True), *self.selected_rel_pos(0,1,True))
                        self.y+= 1
                else:
                    if self.grid_block(0,1) == BlockType.Empty:
                        self.y+= 1
                    elif self.grid_block(0,2) == BlockType.Empty and self.grid_block(0,1) != BlockType.No:
                        self.y+= 1
                        self.swap_grid_block(self.x, self.y, self.x, self.y+1)
                    self.direction = PlayerDir.Down
                    self.select_dir = PlayerDir.Down
            case _:
                ...

font: pygame.font.Font
grid: Grid
player: DevPlayer
indicator: pygame.Surface
grid_size = (9,6)

def initialize(width: int, height: int):
    global font
    font = pygame.font.SysFont("Arial Black", 24)

    global grid, player
    player = DevPlayer(1,2,*grid_size)
    grid = Grid(*grid_size, player)
    player.grid = grid
    grid.set_block(1,1,BlockType.If)
    grid.lock_block(1,1)
    grid.set_block(2,1,BlockType.Glop)
    grid.lock_block(2,1)
    grid.set_block(2,2,BlockType.Death)
    grid.set_block(3,2,BlockType.Equal)
    grid.set_block(4,2,BlockType.Death)
    grid.set_block(5,2,BlockType.Plus)
    grid.set_block(6,2,BlockType.Minus)
    
    grid.set_block(2,3,BlockType.Num_0)
    grid.set_block(3,3,BlockType.Num_1)
    grid.set_block(4,3,BlockType.Num_2)
    grid.set_block(5,3,BlockType.Num_3)
    
    grid.set_block(2,4,BlockType.Coin)
    grid.set_block(3,4,BlockType.Spike)
    

    global indicator
    indicator = pygame.transform.scale_by(pygame.image.load(dev_folder / "blocks" / "mode_dev.png"), 3)

def update(key: int):
    if key:
        if key == pygame.K_w   : player.move(PlayerDir.Up)
        elif key == pygame.K_s : player.move(PlayerDir.Down)
        elif key == pygame.K_d : player.move(PlayerDir.Right)
        elif key == pygame.K_a : player.move(PlayerDir.Left)
        elif key == pygame.K_UP    and player.grid_block(0,-1) != BlockType.Empty and player.grid_block(0,-1) != BlockType.No:
            player.selected = not player.selected
            player.select_dir = PlayerDir.Up
        elif key == pygame.K_DOWN  and player.grid_block(0,1)  != BlockType.Empty and player.grid_block(0,1)  != BlockType.No:
            player.selected = not player.selected
            player.select_dir = PlayerDir.Down
        elif key == pygame.K_RIGHT and player.grid_block(1,0)  != BlockType.Empty and player.grid_block(1,0)  != BlockType.No:
            player.selected = not player.selected
            player.select_dir = PlayerDir.Right
        elif key == pygame.K_LEFT  and player.grid_block(-1,0) != BlockType.Empty and player.grid_block(-1,0) != BlockType.No:
            player.selected = not player.selected
            player.select_dir = PlayerDir.Left
        elif key == pygame.K_SPACE: # auto select
            dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            pdir = [PlayerDir.Up, PlayerDir.Right, PlayerDir.Down, PlayerDir.Left].index(player.select_dir)
            for direction in dirs[pdir:] + dirs[:pdir]:
                if player.grid_block(*direction) != BlockType.Empty and player.grid_block(*direction) != BlockType.No:
                    player.selected = not player.selected
                    player.select_dir = [PlayerDir.Up, PlayerDir.Right, PlayerDir.Down, PlayerDir.Left][dirs.index(direction)]
                    break
        player.tick = 0
    elif player.direction != PlayerDir.Idle:
        player.tick+= 1
        if player.tick > 10:
            player.tick = 0
            player.direction = PlayerDir.Idle

def draw_game(window: pygame.Surface, width:int, height:int):
    window.fill((44,47,63))
    # pygame.draw.rect(window, (0,0,0), (0,0,width*0.05,height))
    # dev mode indicator
    window.blit(indicator, (10,10))

    # draw grid
    grid.draw(window, int(width*0.05), indicator.get_height() + 20, 0, 0)

def main(window: pygame.Surface):
    pygame.font.init()
    width, height = window.get_size()

    initialize(width, height)

    key = 0
    run, clock = True, pygame.time.Clock()
    while run:
        update(key)
        key = 0

        draw_game(window, width, height)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                else:
                    key = event.key

if __name__ == '__main__':
    window = pygame.display.set_mode((1600,900))
    main(window)
    pygame.quit()