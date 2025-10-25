import pygame
import pathlib
pygame.init()

# Loading images
base = pathlib.Path(__file__).parent.parent / "Textures" / "Misc"
exit_button_image: pygame.surface.Surface = pygame.image.load(base / "X.png")
slide_image1: pygame.surface.Surface = pygame.image.load(base / "help_screen.png")
slide_image2: pygame.surface.Surface = pygame.image.load(base / "help_screen2.png")
slide_image3: pygame.surface.Surface = pygame.image.load(base / "help_screen3.png")
slide_image4: pygame.surface.Surface = pygame.image.load(base / "help_screen4.png")

images: list[pygame.surface.Surface] = [
    slide_image1,
    slide_image2,
    slide_image3,
    slide_image4
]

# Colors:
RED: tuple[int, int, int] = (255, 0, 0)
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)

# Font:
FONT = pygame.font.SysFont("Arialblack", 46)


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

    # def button_response(self) -> bool:
    #     if self.cursor_collision() and pygame.mouse.get_pressed()[0] and not self.response_sent:
    #         self.response_sent = True
    #         return True
    #     elif not pygame.mouse.get_pressed()[0]:
    #         self.response_sent = False
    #     return False

class Slide:
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.surface.Surface) -> None:
        self.image = pygame.transform.scale(image, (width, height))
        self.x = x
        self.y = y

    def draw(self, win: pygame.surface.Surface) -> None:
        win.blit(self.image, (self.x, self.y))


exit_button: Button
#left_arrow_button: Button
#right_arrow_button: Button

button_scale: float = 2.5
button_width: int = exit_button_image.get_width()*button_scale
button_height: int = button_width
button_screen_offset: int = 10

slides: list['Slide'] = []
slide_index: int = 0
last_slide_index: int = slide_index
slide_animation_speed: int = 40
slide_position_text: pygame.surface.Surface


def initialize(width: int, height: int) -> None:
    global exit_button, images, slide_position_text

    exit_button = Button(
        width - button_width - button_screen_offset,
        button_screen_offset,
        button_width,
        button_height,
        exit_button_image
    )

    slide_position_text = FONT.render(f"{slide_index+1}/{len(slides)}", 1, (255, 255, 255))

    # left_arrow_button = Button(
    #    button_screen_offset,
    #     height//2 - button_height//2,
    #     button_width,
    #     button_height,
    #     pygame.Surface((1, 1))
    # )

    # right_arrow_button = Button(
    #     width - button_width - button_screen_offset,
    #     height//2 - button_height//2,
    #     button_width,
    #     button_height,
    #     pygame.Surface((1, 1))
    # )

    for image in images:
        slides.append(Slide(0, 0, width, height, image))
        

def update(window: pygame.surface.Surface) -> str:
    global slide_index, last_slide_index, slide_position_text
    if exit_button.cursor_collision():
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if pygame.key.get_pressed()[pygame.K_RIGHT] and slide_index < (len(slides) -1) and slides[slide_index].x == 0:
        last_slide_index = slide_index
        slide_index += 1
        slides[slide_index].x = window.get_width()
    elif pygame.key.get_pressed()[pygame.K_LEFT] and slide_index > 0 and slides[slide_index].x == 0:
        last_slide_index = slide_index
        slide_index -= 1
        slides[slide_index].x = 0 - window.get_width()

    if slides[slide_index].x < 0: # to right
        slides[slide_index].x = min(0, slides[slide_index].x+slide_animation_speed)
        slides[last_slide_index].x = min(slides[last_slide_index].x+slide_animation_speed, window.get_width())
    if slides[slide_index].x > 0: # to left
        slides[slide_index].x = max(0, slides[slide_index].x-slide_animation_speed)
        slides[last_slide_index].x = max(0 - window.get_width(), slides[last_slide_index].x-slide_animation_speed)

    slide_position_text = FONT.render(f"{slide_index+1}/{len(slides)}", 1, (255, 255, 255))

    if exit_button.update(): return "exit"
    return ""

# def report_activity() -> str:
#     if exit_button.button_response():
#         return "help_exit"
#     return ""


def draw(window: pygame.surface.Surface) -> None:
    window.fill(WHITE)
    if slides[slide_index].x != 0:
        slides[last_slide_index].draw(window)
        slides[slide_index].draw(window)
    else:
        slides[slide_index].draw(window)

    exit_button.draw(window)
    window.blit(slide_position_text, (button_screen_offset*2, button_screen_offset))
    #left_arrow_button.draw(window)
    #right_arrow_button.draw(window)


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
