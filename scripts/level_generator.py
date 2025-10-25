import pygame, json
from enum import Enum, auto

class BlockType(Enum):
    AIR = auto()
    GROUND = auto()
    PLATFORM = auto()
    SPIKE = auto()
    DOOR = auto()
    COIN = auto()

image_scale = 4
block_size = 32 * image_scale

class Block:
    def __init__(self, block_type: 'BlockType') -> None:
        self.type = block_type
        self.texture: pygame.surface.Surface

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.grid = [[Block(BlockType.AIR) for _ in range(width)] for _ in range(height)]
        self.door_pos = None
        self.coin_pos = None

    def get_block(self, x: int, y: int) -> 'BlockType':
        return self.grid[y][x].type

    def set_block(self, x: int, y: int, block_type: 'BlockType') -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        if block_type == BlockType.DOOR:
            if self.door_pos is not None:
                old_x, old_y = self.door_pos
                self.grid[old_y][old_x].type = BlockType.AIR
            self.door_pos = (x, y)

        elif block_type == BlockType.COIN:
            if self.coin_pos is not None:
                old_x, old_y = self.coin_pos
                self.grid[old_y][old_x].type = BlockType.AIR
            self.coin_pos = (x, y)

        self.grid[y][x].type = block_type

    def draw(self, win: pygame.surface.Surface, offsetx: int, width: int) -> None:
        nsurf = pygame.Surface((width, win.get_height()), pygame.SRCALPHA)

        for y in range(self.height):
            for x in range(self.width):
                bx = x * block_size - offsetx
                by = y * block_size

                btype = self.grid[y][x].type

                if btype == BlockType.GROUND:
                    pygame.draw.rect(nsurf, (0, 0, 0), (bx, by, block_size, block_size))
                elif btype == BlockType.PLATFORM:
                    pygame.draw.rect(nsurf, (0, 0, 0), (bx, by, block_size, block_size // 3))
                elif btype == BlockType.SPIKE:
                    pygame.draw.rect(nsurf, (200, 0, 0), (bx, by + (block_size * 2) // 3, block_size, block_size // 3))
                elif btype == BlockType.DOOR:
                    pygame.draw.rect(nsurf, (139, 69, 19), (bx, by, block_size, block_size))
                elif btype == BlockType.COIN:
                    pygame.draw.circle(nsurf, (255, 215, 0), (bx + block_size // 2, by + block_size // 2), block_size // 3)

                # outline for all tiles
                pygame.draw.rect(nsurf, (200, 200, 200), (bx, by, block_size, block_size), 2)

        win.blit(nsurf, (0, 0))


selected_material = BlockType.AIR

def sel_bar():
    """Selection bar on the right side of the screen"""
    global selected_material
    mouse = pygame.mouse.get_pos()
    mousedown = pygame.mouse.get_pressed()[0]

    # sidebar background
    pygame.draw.rect(window, (150, 150, 150), (1300, 0, 300, 900), border_radius=5)

    # buttons for each block type
    buttons = [
        (BlockType.AIR, "Air Block"),
        (BlockType.GROUND, "Ground Block"),
        (BlockType.PLATFORM, "Platform Block"),
        (BlockType.SPIKE, "Spike Block"),
        (BlockType.DOOR, "Door Block"),
        (BlockType.COIN, "Coin Block"),
    ]

    for i, (btype, label) in enumerate(buttons):
        rect = pygame.Rect(1350, 50 + i * 110, 200, 90)
        text = font.render(label, True, (0, 0, 0))

        if selected_material == btype:
            color = (100, 100, 100)
        elif rect.collidepoint(mouse):
            color = (170, 170, 170)
        else:
            color = (200, 200, 200)

        pygame.draw.rect(window, color, rect, border_radius=5)
        window.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        # click detection
        if rect.collidepoint(mouse) and mousedown:
            selected_material = btype

def get_grid():
    height, width = grid.height, grid.width
    conversion = {
        BlockType.AIR : "A",
        BlockType.GROUND : "G",
        BlockType.PLATFORM : "P",
        BlockType.SPIKE : "S",
        BlockType.DOOR : "D",
        BlockType.COIN : "C"
    }
    # n_grid = [[grid.grid[y][x].type.name for x in range(width)] for y in range(height)]
    # with open("grid_file.json","w") as f:
    #     json.dump(n_grid,f)
    end = width-1
    for _ in range(width):
        for y in range(height):
            if grid.get_block(end, y) != BlockType.AIR: break
        else: end-= 1; continue
        break
    end+=1
    n_grid = []
    with open("grid_file.grid","w") as f:
        f.write(f"{end};{height}\n")
        for x in range(end):
            f.write("".join([conversion.get(grid.grid[y][x].type, " ") for y in range(height)]))
            f.write("\n")
        # json.dump(n_grid,f)


# setup
pygame.init()
window = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Selection Bar Example")
font = pygame.font.SysFont("Arial Black", 25)

grid = Grid(100, 7)

run = True
clock = pygame.time.Clock()
offx = 0

while run:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        offx -= 5
    if keys[pygame.K_d]:
        offx += 5

    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and mx < 1300:
        mx += offx
        mx //= block_size
        my //= block_size
        grid.set_block(mx, my, selected_material)

    window.fill((255, 255, 255))
    grid.draw(window, offx, 1300)
    sel_bar()

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_s:
                get_grid()

pygame.quit()
