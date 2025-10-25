import pygame
from enum import Enum, auto
import pathlib
pygame.mixer.init()

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
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x].type
        return BlockType.No
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
                img = self.imgs.get_image(self.get_block(x,y))
                if self.get_block(x,y) == BlockType.Empty and self.get_block(x,y-1) == BlockType.If:
                    img = self.imgs.get_image(BlockType.Arrow_right)
                if self.get_block(x,y) != BlockType.No:
                    nsurf.blit(img, (x * block_size - scroll_x, y * block_size - scroll_y))
                if self.grid[y][x].locked:
                    nsurf.blit(self.imgs.get_image(BlockType.Locked), (x * block_size - scroll_x, y * block_size - scroll_y))

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

    def safeeval(self, text: str):
        try:
            return eval(text, {}, {})
        except Exception:
            return None

    def convert_to_val(self, parameters: list[str]) -> list[str]:
        tokens = {
            "Plus": "+",
            "Minus": "-",
            "Equal": "==",
            "Not": " not ",
        }
        out = []
        for token in parameters:
            if token.startswith("Num_"):
                out.append(token[4:])
            else:
                out.append(tokens.get(token, token))
        return out

    def execute_order(self, actions: list[str]) -> dict:
        """
        Handles commands and assignments.
        Example:
          [Vel, Equal, Num_2]  -> {"vel": 2}
          [Jump, Equal, Num_3] -> {"jump": 3}
          [Coin]               -> {"coin_enable": True}
        #   [Death]              -> {"action": "death"}
        """
        rdata = {}

        # 1️⃣ Simple one-block commands
        for ex in actions:
            if ex == "Coin":
                rdata["coin_enable"] = True
            elif ex == "Open":
                rdata["gate_open"] = True
            elif ex == "Close":
                rdata["gate_open"] = False
            # elif ex == "Death":
            #     # Standalone death (not under If)
            #     rdata["action"] = "death"

        # 2️⃣ Assignment type commands
        if len(actions) >= 3 and actions[1] == "Equal":
            variable = actions[0].lower()  # e.g., Vel -> "vel"
            value_expr = "".join(self.convert_to_val(actions[2:]))
            value = self.safeeval(value_expr)
            if value is not None:
                rdata[variable] = value

        return rdata

    def if_chain(self, x:int, y:int):
        parameters: list[str] = []
        for off in range(x, self.grid.width):
            block = self.grid.get_block(off, y)
            if block in (BlockType.Empty, BlockType.No):
                break
            parameters.append(block.name)

        actions = []
        for off in range(x, self.grid.width):
            block = self.grid.get_block(off, y + 1)
            if block in (BlockType.Empty, BlockType.No):
                break
            actions.append(block.name)

        executed = False
        if len(parameters) >= 3:
            parameters = self.convert_to_val(parameters)
            executed = self.safeeval("".join(parameters))
            if executed is None:
                executed = False
            elif "Not" in parameters:
                executed = not executed

        rdata = {}

        # ✅ FIX START — handle conditional Death properly
        if actions:
            # if condition true → execute normally
            if executed:
                rdata.update(self.execute_order(actions))
            # if condition references Death block → mark as on_death trigger
            elif "Death" in parameters or parameters and parameters[0] == "Death":
                rdata["on_death"] = self.execute_order(actions)
        # ✅ FIX END

        print(f"Executed: {executed} : {actions}")
        print(f"---")
        return rdata

    def eval_grid(self):
        data = {}
        under_if = False

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                block = self.grid.get_block(x, y)
                if block in (BlockType.Empty, BlockType.No):
                    under_if = False
                    continue
                if under_if:
                    continue

                # 🟣 1. Handle IF blocks
                if block == BlockType.If:
                    data.update(self.if_chain(x + 1, y))

                # 🟢 2. Handle single top-level commands (Coin, Open, Close)
                elif block in (BlockType.Coin, BlockType.Open, BlockType.Close):
                    result = self.execute_order([block.name])
                    if result:
                        data.update(result)

                # 🔵 3. Handle top-level assignments (Vel, Jump)
                #     Skip if this row belongs to an If chain above.
                elif block in (BlockType.Vel, BlockType.Jump) and (
                    self.grid.get_block(x - 1, y - 1) != BlockType.If
                ):
                    actions = []
                    for off in range(x, self.grid.width):
                        b = self.grid.get_block(off, y)
                        if b in (BlockType.Empty, BlockType.No):
                            break
                        actions.append(b.name)
                    result = self.execute_order(actions)
                    if result:
                        data.update(result)

                # prevent re-evaluation of lower If chains
                if self.grid.get_block(x - 1, y - 1) == BlockType.If:
                    under_if = True
                    continue

        print(data)
        return data



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
        gx = self.x + x
        gy = self.y + y
        if 0 <= gx < self.grid.width and 0 <= gy < self.grid.height:
            if self.grid.grid[gy][gx].locked:
                return BlockType.No
            return self.grid.grid[gy][gx].type
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
processor: GridProcessor
indicator: pygame.Surface
grid_size = (9,6)
instructions_text: pygame.surface.Surface
text_offset: int = 20

def initialize(width: int, height: int):
    global font, instructions_text
    font = pygame.font.SysFont("Arial Black", 24)
    instructions_text = font.render("Press TAB to change MODE", 1, (40, 96, 163))

    global grid, player, processor
    player = DevPlayer(1,2,*grid_size)
    grid = Grid(*grid_size, player)
    player.grid = grid
    grid.set_block(1,1,BlockType.If)
    grid.set_block(2,1,BlockType.Num_1)
    grid.set_block(3,1,BlockType.Equal)
    grid.set_block(4,1,BlockType.Num_1)
    grid.set_block(2,2,BlockType.Vel)
    grid.set_block(2,4,BlockType.Jump)
    grid.set_block(3,2,BlockType.Equal)
    grid.set_block(4,2,BlockType.Num_2)

    grid.set_block(4,3,BlockType.No)

    processor = GridProcessor(grid)

    global indicator
    indicator = pygame.transform.scale_by(pygame.image.load(dev_folder / "blocks" / "mode_dev.png"), 3)

def update(key: int):
    if key:
        if key == pygame.K_w   : player.move(PlayerDir.Up)
        elif key == pygame.K_s : player.move(PlayerDir.Down)
        elif key == pygame.K_d : player.move(PlayerDir.Right)
        elif key == pygame.K_a : player.move(PlayerDir.Left)
        elif key == pygame.K_e : processor.eval_grid()
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
    # dev mode indicator
    window.blit(indicator, (10,10))

    # draw grid
    grid.draw(window, int(width*0.05), indicator.get_height() + 20, 0, 0)
    window.blit(instructions_text, (width-instructions_text.get_width()-text_offset*2, text_offset))

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