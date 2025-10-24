import pygame, pathlib

class Platform:
    def __init__(self, x: float, y: float, w: int, h: int, col: tuple[int,int,int]) -> None:
        self.color = col
        self.x, self.y, self.width, self.height = x,y,w,h
    
    @property
    def rect(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)
    @rect.setter
    def rect(self, value: pygame.rect.Rect):
        self.x, self.y, self.width, self.height = int(value.x), int(value.y), int(value.w), int(value.h)

    def draw(self, win: pygame.surface.Surface) -> None:
        pygame.draw.rect(win, self.color, self.rect)

class Player:
    def __init__(self, x: float, y: float, w: int, h: int, col: tuple[int,int,int], tex: list[pathlib.Path]) -> None:
        self.width, self.height = w, h
        self.color = col

        self.x, self.y = x, y
        self.x_vel, self.y_vel = 0, 0

        self.texture_counter = 0
        self.textures = [pygame.transform.scale_by(pygame.image.load(tex_path),4) for tex_path in tex]
        self.cur_texture = 0

    @property
    def rect(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)
    @rect.setter
    def rect(self, value: pygame.rect.Rect):
        self.x, self.y, self.width, self.height = int(value.x), int(value.y), int(value.w), int(value.h)

    def draw(self, win: pygame.surface.Surface) -> None:
        # pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.textures[self.cur_texture],self.rect)

    def update(self, keys: pygame.key.ScancodeWrapper ,platforms: list[Platform]) -> None:
        if keys[pygame.K_w]: self.y_vel = - P_JUMP
        if keys[pygame.K_a]: self.x_vel -= P_SPEED
        if keys[pygame.K_d]: self.x_vel += P_SPEED
        # velocity
        self.y_vel += gravity
        self.x_vel *= P_SLIDE

        for platform in platforms: # x
            if platform.rect.colliderect(self.rect):
                self.x_vel = 0
                break
        else:
            self.x += self.x_vel

        for platform in platforms: # y
            if platform.rect.colliderect(self.rect):
                self.y_vel = 0
                break
        else:
            self.y += self.y_vel

        # texture
        self.texture_counter += 1
        if self.texture_counter == 120:
            self.cur_texture = (self.cur_texture + 1) % len(self.textures)

################################################################################################################

# def check_keys(player: Player) -> None:
#     keys_pressed = pygame.key.get_pressed()

#     if keys_pressed[pygame.K_w]: player.y_vel = - P_JUMP
#     if keys_pressed[pygame.K_a]: player.x_vel -= P_SPEED
#     if keys_pressed[pygame.K_d]: player.x_vel += P_SPEED

def draw(win: pygame.surface.Surface, player: Player, platforms: list[Platform]) -> None:
    for platform in platforms:
        platform.draw(win)

    player.draw(win)

def update(player: Player, platforms: list[Platform]) -> None:
    keys = pygame.key.get_pressed()
    # check_keys(player)
    player.update(keys, platforms)

################################################################################################################

def main(window: pygame.surface.Surface):
    # width, height = window.get_size()

    player = Player(0, 0, P_W, P_H, P_COL, P_TEX)
    platforms = [Platform(50, 800, 1500, 50, (0, 255, 255))]

    run, clock = True, pygame.time.Clock()
    while run:
        window.fill((0,0,0))

        draw(window, player, platforms)
        update(player, platforms)

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
    P_COL = (255,255,255)
    P_JUMP = 20
    P_SPEED = 5
    P_SLIDE = 0.8

    base = pathlib.Path(__file__).parent.parent / "Textures"
    P_TEX = [
        base / "Glop.png",
        base / "glop_idle2.png"
    ]

    gravity = 0

    window = pygame.display.set_mode((1600,900))

    main(window)
    pygame.quit()