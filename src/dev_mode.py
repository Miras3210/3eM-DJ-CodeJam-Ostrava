import pygame
from enum import Enum, auto
import pathlib

class BlockType(Enum):
    Air = auto()
    Arrow_right = auto()
    No = auto()
    Coin = auto()
    Close = auto()
    Death = auto()
    Empty = auto()
    Equal = auto()
    Glop = auto()
    Grass = auto()
    Honey = auto()
    Ice = auto()
    If = auto()
    Jump = auto()
    Key = auto()
    Locked = auto()
    Minus = auto()
    Not = auto()
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
    Vel = auto()
    Touch = auto()
    Open = auto()
    X = auto()
    Y = auto()

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
            BlockType.Air    : _img_load_helper(block_folder / "air_block.png", block_size),
            BlockType.Arrow_right: _img_load_helper(block_folder / "arrow_right.png", block_size),
            BlockType.Close  : _img_load_helper(block_folder / "close_block.png", block_size),
            BlockType.Coin   : _img_load_helper(block_folder / "coin_block.png", block_size),
            BlockType.Death  : _img_load_helper(block_folder / "death_block.png", block_size),
            BlockType.Empty  : _img_load_helper(block_folder / "dev_block.png", block_size),
            BlockType.Equal  : _img_load_helper(block_folder / "equal_block.png", block_size),
            BlockType.Glop   : _img_load_helper(block_folder / "glop_block.png", block_size),
            BlockType.Grass  : _img_load_helper(block_folder / "grass_block.png", block_size),
            BlockType.Honey  : _img_load_helper(block_folder / "honey_block.png", block_size),
            BlockType.Ice    : _img_load_helper(block_folder / "ice_block.png", block_size),
            BlockType.If     : _img_load_helper(block_folder / "if_block.png", block_size),
            BlockType.Jump   : _img_load_helper(block_folder / "jump_block.png", block_size),
            BlockType.Key    : _img_load_helper(block_folder / "key_block.png", block_size),
            BlockType.Locked : _img_load_helper(block_folder / "locked_overlay.png", block_size),
            BlockType.Minus  : _img_load_helper(block_folder / "minus_block.png", block_size),
            BlockType.Not    : _img_load_helper(block_folder / "not_block.png", block_size),
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
            BlockType.Open   : _img_load_helper(block_folder / "open_block.png", block_size),
            BlockType.Plus   : _img_load_helper(block_folder / "plus_block.png", block_size),
            BlockType.Selected:_img_load_helper(block_folder / "selected_overlay.png", block_size),
            BlockType.Spike  : _img_load_helper(block_folder / "spike_block.png", block_size),
            BlockType.Touch  : _img_load_helper(block_folder / "touch_block.png", block_size),
            BlockType.Vel    : _img_load_helper(block_folder / "speed_block.png", block_size),
            BlockType.X      : _img_load_helper(block_folder / "x_block.png", block_size),
            BlockType.Y      : _img_load_helper(block_folder / "y_block.png", block_size),
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

class GridProcessor:
    def __init__(self, grid: 'Grid') -> None:
        self.grid = grid
    def if_chain(self, x:int,y:int):
        parameters: list[str] = []
        for off in range(x, self.grid.width):
            block = self.grid.get_block(off,y)
            if block == BlockType.Empty:
                break
            parameters.append(block.name)
        execution = []
        for off in range(x, self.grid.width):
            block = self.grid.get_block(off,y+1)
            if block == BlockType.Empty:
                break
            execution.append(block.name)
        
        executed = False
        if len(parameters) >= 3:
            for i in range(len(parameters)):
                if parameters[i].startswith("Num_"):
                    parameters[i] = parameters[i][4:]
                parameters[i] = parameters[i].replace("Plus", "+").replace("Equal", "==").replace("Minus", "-")
            try:
                executed = eval("".join(parameters), {}, {})
                if parameters.__contains__("Not"):
                    executed = not executed
            except Exception:
                executed = False

        print(f"If-valid: {executed}")
        print(f"if_execute: {execution}")
        print(f"---")
    def eval_grid(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                block = self.grid.get_block(x,y)
                if block == BlockType.If:
                    self.if_chain(x+1,y)

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
process: GridProcessor
indicator: pygame.Surface
grid_size = (9,6)

def initialize(width: int, height: int):
    global font
    font = pygame.font.SysFont("Arial Black", 24)

    global grid, player, process
    player = DevPlayer(1,2,*grid_size)
    grid = Grid(*grid_size, player)
    player.grid = grid
    grid.set_block(1,1,BlockType.If)
    grid.set_block(2,1,BlockType.Num_1)
    grid.set_block(3,1,BlockType.Plus)
    grid.set_block(4,1,BlockType.Num_1)
    grid.set_block(5,1,BlockType.Equal)
    grid.set_block(6,1,BlockType.Num_2)
    grid.set_block(2,2,BlockType.Coin)
    grid.lock_block(2,2)
    grid.lock_block(1,1)

    process = GridProcessor(grid)
    
    global indicator
    indicator = pygame.transform.scale_by(pygame.image.load(dev_folder / "blocks" / "mode_dev.png"), 3)

def update(key: int):
    if key:
        if key == pygame.K_w   : player.move(PlayerDir.Up)
        elif key == pygame.K_s : player.move(PlayerDir.Down)
        elif key == pygame.K_d : player.move(PlayerDir.Right)
        elif key == pygame.K_a : player.move(PlayerDir.Left)
        elif key == pygame.K_e : process.eval_grid()
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

    if key == pygame.K_TAB: return "switch"
    return ""

def draw_game(window: pygame.Surface):
    window.fill((44,47,63))
    width, height = window.get_size()
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

        draw_game(window)
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