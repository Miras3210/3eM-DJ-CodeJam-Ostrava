import pygame
import random
from pathlib import Path
from enum import Enum, auto
pygame.display.init()
pygame.mixer.init()

music_dir = Path(__file__).parent.parent / "Music" / "Musik"
theme = music_dir / "AmbientPlatformer.mp3"
pygame.mixer.music.load(theme)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

class BlockType(Enum):
    AIR = auto()
    GROUND = auto()
    PLATFORM = auto()
    SPIKE = auto()
    COIN = auto()
    DOOR = auto()
    NO = auto()

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
sound_dir = Path(__file__).parent.parent / "Music"
effect_dir = sound_dir / "SoudEffects"
music_dir = sound_dir / "Musik"

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

pygame.mixer.music.set_volume(0.7)

class SoundEffects:
    walk     =pygame.mixer.Sound(effect_dir / "walk.wav")
    fall     =pygame.mixer.Sound(effect_dir / "fall.wav")
    death    =pygame.mixer.Sound(effect_dir / "death.wav")
    jump     =pygame.mixer.Sound(effect_dir / "jump.wav")

class Music:
    developer   = pygame.mixer.Sound(music_dir / "AmbientDeveloper.wav")
    menu        = pygame.mixer.Sound(music_dir / "AmbientMenu.wav")
    platformer  = pygame.mixer.Sound(music_dir / "AmbientPlatformer.mp3")

block_dir = adventure_dir / "blocks"

class BlockImages:
    air                = _img_load_helper(block_dir / "air.png")
    cloud1             = _img_load_helper(block_dir / "cloud1.png")
    cloud2             = _img_load_helper(block_dir / "cloud2.png")
    cloud3             = _img_load_helper(block_dir / "cloud3.png")
    dirt_block         = _img_load_helper(block_dir / "dirt_block.png")
    grass              = _img_load_helper(block_dir / "grass.png")
    grass_inner_corner = _img_load_helper(block_dir / "grass_inner_corner.png")
    grass_outer_corner = _img_load_helper(block_dir / "grass_outer_corner.png")
    grass_block        = _img_load_helper(block_dir / "grass_block.png")
    platform           = _img_load_helper(block_dir / "platform.png")
    spikes             = _img_load_helper(block_dir / "spikes.png")
    coin               = _img_load_helper(block_dir / "Coin.png")
    door               = _img_load_helper(block_dir / "door.png")
    gbush              = _img_load_helper(block_dir / "gbush.png")
    short_grass        = _img_load_helper(block_dir / "short_grass.png")
    rock               = _img_load_helper(block_dir / "rock.png")
    michal               = _img_load_helper(block_dir / "michal.png")


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
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].type
        else:
            return BlockType.NO

    def set_block(self, x: int, y: int, block_type: 'BlockType') -> None:
        self.grid[y][x].type = block_type

    def bake_textures(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].type == BlockType.GROUND:
                    # pygame.draw.rect(win, (0,0,0), (0,0))
                    self.grid[y][x].texture.blit(BlockImages.dirt_block, (0,0))
                    if y>0 and self.get_block(x,y-1) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(BlockImages.grass, (0,0))
                    if x>0 and self.get_block(x-1, y) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,90), (0,0))
                    if x>0 and self.get_block(x-1, y) != BlockType.GROUND and y>0 and self.get_block(x,y-1) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_outer_corner,90), (0,0))

                    if y>0 and self.get_block(x, y+1) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,180), (0,0))
                    if x>0 and self.get_block(x+1, y) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass,270), (0,0))
                    if x>0 and self.get_block(x+1, y) != BlockType.GROUND and self.get_block(x, y+1) != BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_outer_corner,270), (0,0))

                    if self.get_block(x+1, y-1) != BlockType.GROUND and self.get_block(x, y-1) == BlockType.GROUND and self.get_block(x+1, y) == BlockType.GROUND:
                        self.grid[y][x].texture.blit(BlockImages.grass_inner_corner, (0,0))
                    if self.get_block(x-1, y-1) != BlockType.GROUND and self.get_block(x, y-1) == BlockType.GROUND and self.get_block(x-1, y) == BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_inner_corner,90), (0,0))
                    if self.get_block(x-1, y+1) != BlockType.GROUND and self.get_block(x, y+1) == BlockType.GROUND and self.get_block(x-1, y) == BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_inner_corner,180), (0,0))
                    if self.get_block(x+1, y+1) != BlockType.GROUND and self.get_block(x, y+1) == BlockType.GROUND and self.get_block(x+1, y) == BlockType.GROUND:
                        self.grid[y][x].texture.blit(pygame.transform.rotate(BlockImages.grass_inner_corner,270), (0,0))

                if self.get_block(x, y) == BlockType.PLATFORM:
                    self.grid[y][x].texture.blit(BlockImages.platform, (0,0))

                if self.get_block(x, y) == BlockType.SPIKE:
                    self.grid[y][x].texture.blit(BlockImages.spikes, (0,0))

                if self.get_block(x, y) == BlockType.COIN:
                    self.grid[y][x].texture.blit(BlockImages.coin, (0,0))

                if self.get_block(x, y) == BlockType.DOOR:
                    self.grid[y][x].texture.blit(BlockImages.door, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,25):
                    self.grid[y][x].texture.blit(BlockImages.cloud1, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,25):
                    self.grid[y][x].texture.blit(BlockImages.cloud2, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,25):
                    self.grid[y][x].texture.blit(BlockImages.cloud3, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,4) and self.get_block(x, y+1) == BlockType.GROUND and y>0:
                    self.grid[y][x].texture.blit(BlockImages.gbush, (0,0))

                if self.get_block(x, y) == BlockType.AIR and self.get_block(x, y+1) == BlockType.GROUND and y>0:
                    self.grid[y][x].texture.blit(BlockImages.short_grass, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,6) and self.get_block(x, y+1) == BlockType.GROUND and y>0:
                    self.grid[y][x].texture.blit(BlockImages.rock, (0,0))

                if self.get_block(x, y) == BlockType.AIR and not random.randint(0,1000) and self.get_block(x, y+1) == BlockType.GROUND and y>0:
                    self.grid[y][x].texture.blit(BlockImages.michal, (0,0))

    def draw(self, win: pygame.surface.Surface, offsetx: int) -> None:
        for y in range(self.height):
            for x in range(self.width):
                win.blit(self.grid[y][x].texture, (x*block_size-offsetx,y*block_size,block_size,block_size))

class Player:
    def __init__(self) -> None:
        self.x, self.y = 0,0
        self.width, self.height = block_size, block_size
        self.x_vel, self.y_vel = 0, 0

        self.grid: 'Grid'

        self.on_wall, self.on_ground = False, False
        self.alive = True
        self.win = False

        self.afk_counter = 0
        self.on_ground_counter = 0
        self.move_counter = 0
        self.coin_counter = 0

        self.SPEED = 3
        self.JUMP = 30
        self.SLIDE = 0.8
        self.VOID = 1500

    @property
    def hitbox(self) -> pygame.Rect:
        return pygame.Rect(self.x+16, self.y+36, self.width-32, self.height-36)

    def draw(self, win: pygame.surface.Surface, offsetx: int) -> None:
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
        win.blit(texture,(self.x-offsetx, self.y))
        
    def sound(self, effect: pygame.mixer.Sound, volume: float) -> None:
        effect.set_volume(volume)
        effect.play()

    def update(self, keys: pygame.key.ScancodeWrapper, param: dict) -> None:
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if self.on_ground:
                self.sound(SoundEffects.jump, 0.2)
                self.y_vel = -(self.JUMP * param.get("jump", 1))

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_vel -= (self.SPEED * param.get("vel", 1))
            self.move_counter += 1
            
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_vel += (self.SPEED * param.get("vel", 1))
            self.move_counter += 1

    # velocity
        self.y_vel += gravity
        if abs(self.x_vel) < 0.1: self.x_vel = 0
        else: self.x_vel *= self.SLIDE

    # collision
        self.x_updated_rect = self.hitbox
        self.x_updated_rect.x += int(self.x_vel)
        for y, line in enumerate(self.grid.grid):
            for x, block in enumerate(line):
                if (block.type == BlockType.GROUND and self.x_updated_rect.colliderect((x*block_size, y*block_size, block_size, block_size))) \
                    or (block.type == BlockType.PLATFORM and self.x_updated_rect.colliderect((x*block_size, y*block_size, block_size, 36))) \
                    or (self.x_updated_rect.x < 0):
                    self.x_vel = 0
                    self.on_wall = True
                    break
            else: continue
            break
        else:
            self.x += int(self.x_vel)
            self.on_wall = False
        self.y_updated_rect = self.hitbox
        self.y_updated_rect.y += int(self.y_vel)
        for y, line in enumerate(self.grid.grid):
            for x, block in enumerate(line):
                if block.type == BlockType.SPIKE and self.hitbox.colliderect((x*block_size, y*block_size+82, block_size, 36)):
                    self.alive = False
                    self.sound(SoundEffects.death, 0.1)
                if block.type == BlockType.DOOR and self.hitbox.colliderect((x*block_size, y*block_size, block_size, block_size)):
                    self.win = True
                if block.type == BlockType.COIN and self.hitbox.colliderect((x*block_size+20, y*block_size+20, block_size-40, block_size-40)):
                    self.coin_counter += 1
                if (block.type == BlockType.GROUND and self.y_updated_rect.colliderect((x*block_size, y*block_size, block_size, block_size))) \
                  or (self.y_vel > 0 and self.hitbox.bottom <= y*block_size and block.type == BlockType.PLATFORM and self.y_updated_rect.colliderect((x*block_size, y*block_size, block_size, 36))):
                    if self.hitbox.bottom <= y*block_size:
                        self.on_ground = True
                        self.y_updated_rect.bottom = y*block_size
                        self.y = self.y_updated_rect.y - 36
                    self.y_vel = 0
                    if self.on_ground and self.on_ground_counter < 150:
                        self.on_ground_counter+= 1
                    break
            else: continue
            break
        else:
            self.y += int(self.y_vel)
            self.on_ground = False
            self.on_ground_counter = 0
        
        if self.y > self.VOID:
            self.alive = False
            self.sound(SoundEffects.death, 0.1)
            # self.y_vel = 0
        
        if self.y_vel == 0 and self.x_vel == 0:
            self.afk_counter+= 1
            self.move_counter = 0
            if self.afk_counter == 180:
                self.afk_counter = 120
        else:
            self.afk_counter = 0
            
        if self.move_counter >= 10 and self.on_ground:
            self.sound(SoundEffects.walk, 0.1)
            self.move_counter = -10
            
        if self.on_ground_counter == 1:
            self.sound(SoundEffects.fall, 0.1)

################################################################################################################

Level_dir = Path(__file__).parent.parent / "Levels"

pygame.font.init()
font = pygame.font.SysFont("Arial Black", 24)
player: Player
grid: Grid
indicator: pygame.Surface
level = 1
gravity = 1.5

camx = 0

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
        s = f.readline().strip().split(";")
        grid.regenerate(int(s[0]), int(s[1]))

        for x, line in enumerate(f):
            for y, bl in enumerate(line.strip()):
                grid.set_block(x,y,grid_legend.get(bl, BlockType.AIR))
    grid.bake_textures()

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
    load_level(level, grid)

    player = Player()
    player.grid = grid

    global indicator
    indicator = pygame.transform.scale_by(pygame.image.load(adventure_dir / "blocks" / "mode_game.png"), 3)


def draw(win: pygame.surface.Surface) -> None:
    win.fill((255,255,255))

    grid.draw(win, camx)
    player.draw(win, camx)

    win.blit(indicator, (10,10))
    
    win.blit(font.render(f"1: {player.afk_counter}", 1, (0,0,0)), (10, 30))
    win.blit(font.render(f"2: {player.on_ground}", 1, (0,0,0)), (10, 50))
    win.blit(font.render(f"3: {player.y_vel}", 1, (0,0,0)), (10, 70))

def update(key: int, screen_width: int, param: dict) -> str:
    global camx
    keys = pygame.key.get_pressed()
    player.update(keys, param)

    camx = int(min(max(0, (camx+player.x-player.width*3)/2), grid.width*block_size - screen_width))

    if not player.alive: return "bsod"
    if player.win: return "next"
    if key == pygame.K_TAB: return "switch"
    return ""

################################################################################################################

def main(window: pygame.surface.Surface):
    width, height = window.get_size()
    run, clock = True, pygame.time.Clock()
    initialize(width, height)
    key = 0
    while run:
        # update(key, width)
        key = 0

        draw(window)

        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                key = event.key


if __name__ == '__main__':
    # globals
    window = pygame.display.set_mode((1600,900))

    main(window)
    pygame.quit()