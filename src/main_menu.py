import pygame
import pathlib

# Image load:
base = pathlib.Path(__file__).parent.parent / "Textures" / "Misc"
background_image: pygame.surface.Surface = pygame.image.load(base / "main_screen.png")
help_button_image: pygame.surface.Surface = pygame.image.load(base / "help_button.png")
start_button_image: pygame.surface.Surface = pygame.image.load(base / "start_button.png")
quit_button_image: pygame.surface.Surface = pygame.image.load(base / "quit_button.png")
logo_image: pygame.surface.Surface = pygame.image.load(base / "studio_logo.png")

# Colors:
BLACK: tuple[int, int, int] = (0, 0, 0)


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface, max_hover_scale: float = 1.2) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        self.scale = 1
        self.response_sent = False
        self.max_hover_scale = max_hover_scale

    def draw(self, win: pygame.surface.Surface) -> None:
        if self.scale != 1:
            anim_rect = pygame.Rect(
                self.rect.x - (self.rect.width*(self.scale-1))/2,
                self.rect.y - (self.rect.height*(self.scale-1))/2,
                self.rect.width*self.scale,
                self.rect.height*self.scale
            )
            win.blit(pygame.transform.scale(self.image, (anim_rect.width, anim_rect.height)), (anim_rect.x, anim_rect.y))
        else:
            win.blit(pygame.transform.scale(self.image, (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y))

    def cursor_collision(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self) -> bool:
        if self.cursor_collision():
            self.scale = min(self.max_hover_scale, self.scale+0.02)
            return pygame.mouse.get_pressed()[0]
        else:
            self.scale = max(1, self.scale-0.02)
        return False


start_button: Button
help_button: Button
quit_button: Button
background: pygame.surface.Surface
logo: pygame.surface.Surface

button_scale: int = 5
start_button_width: int = 64*button_scale
side_button_width: int = 64*button_scale
start_button_height: int = 32*button_scale
side_button_height: int = 32*button_scale
x_shift: int = 210
y_shift: int = 80
logo_width: int = 200
logo_height: int = logo_width
x_logo_offset: int = 40
y_logo_offset: int = x_logo_offset//8

transition_animation: bool = False
animation_scale: int = 0
after_help_button: bool = False
after_start_button: bool = False
start_button_active: bool = False
help_button_active: bool = False


def initialize(width: int, height: int) -> None:
    global start_button, help_button, quit_button, background, logo
    background = pygame.transform.scale(background_image, (width, height))
    logo = pygame.transform.scale(logo_image, (logo_width, logo_height))

    help_button = Button(
        width//3//2 - side_button_width//2 + x_shift + 2,
        height//2 - side_button_height//2 + y_shift,
        side_button_width,
        side_button_height, 
        help_button_image
    )
    start_button = Button(
        width//2 - start_button_width//2,
        height//2 - start_button_height//2 + y_shift,
        start_button_width, 
        start_button_height,
        start_button_image
    )
    quit_button = Button(
        width//3*2 + width//3//2 - side_button_width//2 - x_shift,
        height//2 - side_button_height//2 + y_shift,
        side_button_width,
        side_button_height, 
        quit_button_image
    )


def update(window: pygame.surface.Surface) -> str:
    global transition_animation, animation_scale, after_start_button, after_help_button, start_button_active, help_button_active
    if any([start_button.cursor_collision(),
            help_button.cursor_collision(),
            quit_button.cursor_collision()]):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # if start_button.button_response():
    #     transition_animation = True
    #     after_start_button = True
    # elif help_button.button_response():
    #     transition_animation = True
    #     after_help_button = True

    if transition_animation:
        animation_scale += 26
        if animation_scale > window.get_width()//2 + window.get_width()//3:
            transition_animation = False
            if after_start_button:
                start_button_active = True
            elif after_help_button:
                help_button_active = True
    else:
        after_help_button = False
        after_start_button = False
        animation_scale = 0

    if start_button.update():
        # transition_animation = True
        # after_start_button = True
        return "play"
    if help_button.update():
        # transition_animation = True
        # after_help_button = True
        return "help"
    if quit_button.update(): return "quit"
    return ""

# def report_activity() -> str:
#     global start_button_active, help_button_active
#     if quit_button.button_response():
#         return "quit"
#     if start_button_active:
#         start_button_active = False
#         return "play"
#     if help_button_active:
#         help_button_active = False
#         return "help"
#     return ""


def draw(window: pygame.surface.Surface) -> None:
    global transition_animation, animation_scale, after_help_button, after_start_button
    window.blit(background, (0, 0))
    window.blit(logo, (window.get_width() - logo_width - x_logo_offset, window.get_height() - logo_height - y_logo_offset))
    start_button.draw(window)
    help_button.draw(window)
    quit_button.draw(window)
    if transition_animation:
        pygame.draw.circle(window, BLACK, (window.get_size()[0]//2, window.get_size()[1]//2), animation_scale)
        

def main(window: pygame.surface.Surface):
    width, height = window.get_size()
    initialize(width, height)

    run, clock = True, pygame.time.Clock()
    while run:
        update(window)
        draw(window)
        
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

if __name__ == '__main__':
    window = pygame.display.set_mode((1600,900))
    main(window)
    pygame.quit()