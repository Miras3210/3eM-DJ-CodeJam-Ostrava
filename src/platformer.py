import pygame
from pathlib import Path
from enum import Enum, auto
pygame.display.init()

class BlockType(Enum):
    AIR = auto()
    GROUND = auto()
    PLATFORM = auto()
    SPIKE = auto()
    COIN = auto()
    DOOR = auto()

class PlayerSprite(Enum):
    Base = auto()
    Idle = auto()
    Right = auto()
    Left = auto()
    Jump = auto()
    Fall = auto()
    Land = auto()

image_scale = 4
block_size = 32 * image_scale
adventure_dir = Path(__file__).parent.parent / "Textures" / "Adventure"
char_dir = adventure_dir / "characters"

def _img_load_helper(img_path: Path) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(img_path), (block_size, block_size))

class PlayerImages:
    Base       = _img_load_helper(char_dir / "Glop.png")
    Idle1      = _img_load_helper(char_dir / "glop_idle1.png")
    Idle2      = _img_load_helper(char_dir / "glop_idle2.png")
    Right      = _img_load_helper(char_dir / "glop_right.png")
    Left       = _img_load_helper(char_dir / "glop_left.png")
    Jump       = _img_load_helper(char_dir / "glop_long.png")
    Jump_Right = _img_load_helper(char_dir / "glop_right_long.png")
    Jump_Left  = _img_load_helper(char_dir / "glop_left_long.png")
    Fall       = _img_load_helper(char_dir / "glop_fall.png")
    Fall_Right = _img_load_helper(char_dir / "glop_right_fall.png")
    Fall_Left  = _img_load_helper(char_dir / "glop_left_fall.png")
    Land       = _img_load_helper(char_dir / "glop_short.png")

block_dir = adventure_dir / "blocks"

class BlockImages:
    air                = _img_load_helper(block_dir / "air.png")
    cloud1             = _img_load_helper(block_dir / "cloud1.png")
    cloud2             = _img_load_helper(block_dir / "cloud2.png")
    dirt_block         = _img_load_helper(block_dir / "dirt_block.png")
    grass              = _img_load_helper(block_dir / "grass.png")
    grass_inner_corner = _img_load_helper(block_dir / "grass_inner_corner.png")
    grass_outer_corner = _img_load_helper(block_dir / "grass_outer_corner.png")
    grass_block        = _img_load_helper(block_dir / "grass_block.png")
    platform           = _img_load_helper(block_dir / "platform.png")
    spikes             = _img_load_helper(block_dir / "spikes.png")
    coin               = _img_load_helper(block_dir / "Coin.png")
    door               = _img_load_helper(block_dir / "door.png")


class Block:
    def __init__(self, block_type: 'BlockType') -> None:
        self.type = block_type
        self.texture: pygame.surface.Surface = BlockImages.air.copy()

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.grid = [[Block(BlockType.AIR) for _ in range(width)] for _ in range(height)]

    def clear_grid(self) -> None:
        for line in self.grid:
            for block in line:
                block.type = BlockType.AIR

    def regenerate(self, width: int, height: int):
        self.width, self.height = width, height
        self.grid = [[Block(BlockType.AIR) for _ in range(width)] for _ in range(height)]

    def get_block(self, x: int, y: int) -> 'BlockType':
        return self.grid[y][x].type

    def set_block(self, x: int, y: int, block_type: 'BlockType') -> None:
        self.grid[y][x].type = block_type

    def bake_textures(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].type == BlockType.GROUND:
                    # pygame.draw.rect(win, (0,0,0), (0,0))
                    self.grid[y][x].texture.blit(BlockImages.dirt_block, (0,0))
                    if y>0 and self.grid[y-1][x].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(BlockImages.grass, (0,0))
                    if x>0 and self.grid[y][x-1].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,90), (0,0))
                    if x>0 and self.grid[y][x-1].type != BlockType.GROUND and y>0 and self.grid[y-1][x].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_outer_corner,90), (0,0))

                    if y>0 and self.grid[y+1][x].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,180), (0,0))
                    if x>0 and self.grid[y][x+1].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,270), (0,0))
                    if x>0 and self.grid[y][x+1].type != BlockType.GROUND and y>0 and self.grid[y+1][x].type != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_outer_corner,270), (0,0))

                    if y>0 and self.grid[y-1][x-1].type != BlockType.GROUND and x>0 and self.grid[y+1][x].type == BlockType.GROUND:
                        self.grid[y][x].texture.blit(BlockImages.grass_inner_corner, (0,0))

                if self.grid[y][x].type == BlockType.PLATFORM:
                    self.grid[y][x].texture.blit(BlockImages.platform, (0,0))

                if self.grid[y][x].type == BlockType.SPIKE:
                    self.grid[y][x].texture.blit(BlockImages.spikes, (0,0))

                if self.grid[y][x].type == BlockType.COIN:
                    self.grid[y][x].texture.blit(BlockImages.coin, (0,0))

                if self.grid[y][x].type == BlockType.DOOR:
                    self.grid[y][x].texture.blit(BlockImages.door, (0,0))

                # pygame.draw.rect(self.grid[y][x].texture, (0,0,0), (0,0,block_size,block_size), 2)

    def draw(self, win: pygame.surface.Surface) -> None:
        for y in range(self.height):
            for x in range(self.width):
                win.blit(self.grid[y][x].texture, (x*block_size,y*block_size,block_size,block_size))

class Player:
    def __init__(self, x: float, y: float, w: int, h: int) -> None:
        self.width, self.height = w, h
        self.x, self.y = x, y
        self.x_vel, self.y_vel = 0, 0

        self.grid: 'Grid'

        self.on_wall, self.on_ground = False, False

        self.afk_counter = 0
        self.on_ground_counter = 0

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.x+16, self.y, self.width-32, self.height)

    def draw(self, win: pygame.surface.Surface) -> None:
        texture = PlayerImages.Base
        if not self.on_ground: # in air
            if self.y_vel < 0:
                if self.x_vel > 5:
                    texture = PlayerImages.Jump_Right
                elif self.x_vel < -5:
                    texture = PlayerImages.Jump_Left
                else:
                    texture = PlayerImages.Jump
            else:
                if self.x_vel > 5:
                    texture = PlayerImages.Fall_Right
                elif self.x_vel < -5:
                    texture = PlayerImages.Fall_Left
                else:
                    texture = PlayerImages.Fall
        elif self.on_ground_counter < 10 and abs(self.x_vel) < 5: # just fell down
            texture = PlayerImages.Land
        elif self.x_vel > 5: # right
            texture = PlayerImages.Right
        elif self.x_vel < -5: # left
            texture = PlayerImages.Left
        elif self.afk_counter >= 120:
            texture = PlayerImages.Idle1 if (self.afk_counter // 30) % 2 else PlayerImages.Idle2
        win.blit(texture,(self.x, self.y))

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.on_ground:
                self.y_vel = -P_JUMP
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.x_vel -= P_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.x_vel += P_SPEED

    # velocity
        self.y_vel += gravity
        if abs(self.x_vel) < 0.1: self.x_vel = 0
        else: self.x_vel *= P_SLIDE

    # collision
        self.x_updated_rect = self.hitbox
        self.x_updated_rect.x += int(self.x_vel)
        for y, line in enumerate(self.grid.grid):
            for x, block in enumerate(line):
                if block.type == BlockType.GROUND and self.x_updated_rect.colliderect((x*block_size, y*block_size, block_size, block_size)):
                    self.x_vel = 0
                    self.on_wall = True
                    break
            else: continue
            break
        else:
            if self.x_updated_rect.x > 0:
                self.x += int(self.x_vel)
                self.on_wall = False
            else:
                self.x_vel = 0
                self.on_wall = True

        self.y_updated_rect = self.hitbox
        self.y_updated_rect.y += int(self.y_vel)
        for y, line in enumerate(self.grid.grid):
            for x, block in enumerate(line):
                if block.type == BlockType.GROUND and self.y_updated_rect.colliderect((x*block_size, y*block_size, block_size, block_size)):
                    self.y_vel = 0
                    if self.on_ground and self.on_ground_counter < 150:
                        self.on_ground_counter+= 1
                    self.on_ground = True
                    break
            else: continue
            break
        else:
            self.y += int(self.y_vel)
            self.on_ground = False
            self.on_ground_counter = 0

        if self.y_vel == 0 and self.x_vel == 0:
            self.afk_counter+= 1
            if self.afk_counter == 180:
                self.afk_counter = 120
        else:
            self.afk_counter = 0

################################################################################################################

Level_dir = Path(__file__).parent.parent / "Levels"

pygame.font.init()
font = pygame.font.SysFont("Arial Black", 24)
player: Player
grid: Grid

grid_legend = {
    "A" : BlockType.AIR,
    "G" : BlockType.GROUND,
    "P" : BlockType.PLATFORM,
    "S" : BlockType.SPIKE,
    "D" : BlockType.DOOR,
    "C" : BlockType.COIN
}
def load_grid_file(filename: str | Path, grid: 'Grid'):
    with open(filename,"r") as f:
        for x, line in enumerate(f):
            for y, bl in enumerate(line.strip()):
                grid.set_block(x,y,grid_legend.get(bl, BlockType.AIR))

def load_level(level: int, grid: 'Grid'):
    return load_grid_file(Level_dir / f"Level{level}.grid", grid)

def initialize(width: int, height: int):
    for attr in dir(PlayerImages):
        img = getattr(PlayerImages, attr)
        if isinstance(img, pygame.Surface):
            setattr(PlayerImages, attr, img.convert_alpha())

    for attr in dir(BlockImages):
        img = getattr(BlockImages, attr)
        if isinstance(img, pygame.Surface):
            setattr(BlockImages, attr, img.convert_alpha())
    
    global player, grid
    
    grid = Grid(100,7)
    grid.clear_grid()
    load_level(1, grid)
    print(grid.grid[0][0].texture is grid.grid[0][1].texture)
    grid.bake_textures()
    
    player = Player(0, 0, block_size, block_size)
    player.grid = grid

def draw(win: pygame.surface.Surface, player: Player, grid: Grid) -> None:
    win.fill((255,255,255))

    grid.draw(win)

    player.draw(win)
    win.blit(font.render(f"x: {player.x}", 1, (0,0,0)), (10, 10))
    win.blit(font.render(f"y: {player.y}", 1, (0,0,0)), (10, 35))
    win.blit(font.render(f"afk: {player.y_vel}", 1, (0,0,0)), (10, 60))

def update(player: Player) -> None:
    keys = pygame.key.get_pressed()
    player.update(keys)

################################################################################################################

def main(window: pygame.surface.Surface):
    width, height = window.get_size()
    run, clock = True, pygame.time.Clock()
    initialize(width, height)
    while run:
        update(player)

        draw(window, player, grid)

        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False


if __name__ == '__main__':
    # globals
    P_W, P_H = 128, 128
    P_JUMP = 30
    P_SPEED = 3
    P_SLIDE = 0.8

    gravity = 1.5

    window = pygame.display.set_mode((1600,900))

    main(window)
    pygame.quit()