import pygame

class Platform:
    def __init__(self, x: float, y: float, w: int, h: int, col: tuple[int,int,int]) -> None:
        self.color = col
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    @property
    def x(self) -> int: return self.rect.x
    @x.setter
    def x(self, value: int) -> None: self.rect.x = value
    @property
    def y(self) -> int: return self.rect.y
    @y.setter
    def y(self, value: int) -> None: self.rect.y = value

    @property
    def width(self) -> int: return self.rect.width
    @width.setter
    def width(self, value: int) -> None: self.rect.width = value
    @property
    def height(self) -> int: return self.rect.height
    @height.setter
    def height(self, value: int) -> None: self.rect.height = value

    def draw(self, win: pygame.surface.Surface) -> None:
        pygame.draw.rect(win, self.color, self.rect)

class Player:
    def __init__(self, x: float, y: float, w: int, h: int, col: tuple[int,int,int]) -> None:
        self.width, self.height = w, h
        self.color = col

        self.x, self.y = x, y
        self.x_vel, self.y_vel = 0, 0

        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def move(self, x: float, y: float) -> None:
        self.x += x
        self.y += y
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def collision(self, platform: Platform) -> bool:
        
        if self.x + self.width + self.x_vel > platform.x and self.y + self.height + self.y_vel > platform.y:
            if platform.x + platform.width > self.x + self.x_vel and platform.y + platform.height > self.y + self.y_vel:
                return True
        return False

    def draw(self, win: pygame.surface.Surface) -> None:
        pygame.draw.rect(win, self.color, self.rect)

    def update(self) -> None:
        # velocity
        self.y_vel += gravity
        self.x_vel *= P_SLIDE

        self.move(self.x_vel,self.y_vel)

################################################################################################################

def check_keys(player: Player) -> None:
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_w]: player.y_vel = - P_JUMP
    if keys_pressed[pygame.K_a]: player.x_vel -= P_SPEED
    if keys_pressed[pygame.K_d]: player.x_vel += P_SPEED

def draw(win: pygame.surface.Surface, player: Player, platforms: list[Platform]) -> None:
    for platform in platforms:
        platform.draw(win)

    player.draw(win)

def update(player: Player) -> None:
    check_keys(player)
    player.update()

################################################################################################################

def main(window: pygame.surface.Surface):
    # width, height = window.get_size()

    player = Player(0, 0, P_W, P_H, P_COL)
    platforms = [Platform(50, 800, 1500, 50, (0, 255, 255))]

    run, clock = True, pygame.time.Clock()
    while run:
        window.fill((0,0,0))

        draw(window, player, platforms)
        update(player)

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
    P_W, P_H = 45, 60
    P_COL = (255,255,255)
    P_JUMP = 20
    P_SPEED = 5
    P_SLIDE = 0.8

    gravity = 2

    window = pygame.display.set_mode((1600,900))

    main(window)
    pygame.quit()