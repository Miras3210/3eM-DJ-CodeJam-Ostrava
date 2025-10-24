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
    def __init__(self, x: float, y: float, w: int, h: int, tex_pack: list[list[pathlib.Path]]) -> None:
        self.width, self.height = w, h

        self.x, self.y = x, y
        self.x_vel, self.y_vel = 0, 0
        
        self.on_wall, self.on_ground = False, False
        
        self.texturess = {
            "base": [pygame.transform.scale_by(pygame.image.load(tex_path),4) for tex_path in tex_pack[0]],
            "idle": [pygame.transform.scale_by(pygame.image.load(tex_path),4) for tex_path in tex_pack[1]],
            "move": [pygame.transform.scale_by(pygame.image.load(tex_path),4) for tex_path in tex_pack[2]],
            "jump": [pygame.transform.scale_by(pygame.image.load(tex_path),4) for tex_path in tex_pack[3]]
        }
        self.cur_textures = "base"
        self.cur_texture = 0
        self.state = "base"

        self.texture_counter = 0
        self.stop_counter = 0
        self.fall_counter = 0

    @property
    def rect(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)
    @rect.setter
    def rect(self, value: pygame.rect.Rect):
        self.x, self.y, self.width, self.height = int(value.x), int(value.y), int(value.w), int(value.h)

    def draw(self, win: pygame.surface.Surface) -> None:
        win.blit(self.texturess[self.cur_textures][self.cur_texture],self.rect)

    def update(self, keys: pygame.key.ScancodeWrapper, platforms: list[Platform]) -> None:
        if keys[pygame.K_w]:
            if self.on_ground: self.y_vel = -P_JUMP
        if keys[pygame.K_a]: self.x_vel -= P_SPEED
        if keys[pygame.K_d]: self.x_vel += P_SPEED

        # velocity
        self.y_vel += gravity
        if abs(self.x_vel) < 0.1: self.x_vel = 0
        else: self.x_vel *= P_SLIDE

        self.on_wall = False
        self.x_updated_rect = self.rect
        self.x_updated_rect.x += int(self.x_vel)
        for platform in platforms: # x
            if platform.rect.colliderect(self.x_updated_rect):
                self.x_vel = 0
                self.on_wall = True
                break
        else:
            self.x += self.x_vel

        self.on_ground = False
        self.y_updated_rect = self.rect
        self.y_updated_rect.y += int(self.y_vel)
        for platform in platforms: # y
            if platform.rect.colliderect(self.y_updated_rect):
                self.y_vel = 0
                self.on_ground = True
                break
        else:
            self.y += self.y_vel

        # state        
        if self.x_vel == 0 and self.y_vel == 0:
            self.state = "base"
            self.stop_counter += 1

        if not self.x_vel == 0:
            self.state = "move"
            self.stop_counter = 0

        if not self.y_vel == 0 or self.fall_counter < 10:
            self.state = "jump"
            self.stop_counter = 0

        if self.stop_counter > 120:
            self.state = "idle"

        self.cur_textures = self.state

        # texture
        match self.state:
            case "base":
                self.cur_texture = 0

            case "idle":
                self.texture_counter += 1

                if self.texture_counter == 60:
                    self.cur_texture = (self.cur_texture + 1) % len(self.texturess["idle"])
                    self.texture_counter = 0

            case "move":
                if self.x_vel < -5: self.cur_texture = 1
                elif self.x_vel > 5: self.cur_texture = 2
                else: self.cur_texture = 0

            case "jump":
                if self.y_vel < -10: self.cur_texture = 0
                elif self.y_vel > 10: self.cur_texture = 3

                else:
                    if self.on_ground: self.fall_counter += 1
                    else: self.fall_counter = 0
                    self.cur_texture = 6

                if self.x_vel < -5: self.cur_texture += 1
                elif self.x_vel > 5: self.cur_texture += 2

            case _: pass

        if self.state == "idle": self.texture_counter += 1
        if self.texture_counter == 60:
            self.cur_texture = (self.cur_texture + 1) % len(self.texturess["idle"])
            self.texture_counter = 0

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

    player = Player(0, 0, P_W, P_H, P_TEX)
    platforms = [Platform(50, 800, 1500, 50, (0,255,255))]

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
    P_JUMP = 30
    P_SPEED = 3
    P_SLIDE = 0.8

    base = pathlib.Path(__file__).parent.parent / "Textures" / "Adventure" / "characters"
    P_TEX = [
        [
            base / "Glop.png"
        ],
        [
            base / "glop_idle1.png",
            base / "glop_idle2.png"
        ],
        [
            base / "Glop.png",
            base / "glop_left.png",
            base / "glop_right.png"
        ],
        [
            base / "glop_long.png",
            base / "glop_left_long.png",
            base / "glop_right_long.png",
            base / "glop_fall.png",
            base / "glop_left_fall.png",
            base / "glop_right_fall.png",
            base / "glop_short.png",
            base / "glop_left.png",
            base / "glop_right.png"
        ]
    ]
    
    base = pathlib.Path(__file__).parent.parent / "Textures" / "Adventure" / "blocks"
    PLATFORM_TEXTURE = []

    gravity = 2

    window = pygame.display.set_mode((1600,900))

    main(window)
    pygame.quit()