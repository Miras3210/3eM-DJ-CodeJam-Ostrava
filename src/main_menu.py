import pygame


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.surface.Surface) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image

    def draw(self, win: pygame.surface.Surface) -> None:
        win.blit(self.image, self.rect)
        
    def cursor_collision(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def hand_cursor_active(self):
        if self.cursor_collision():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


play_button: Button
help_button: Button
quit_button: Button
title: pygame.image
title_pos: tuple[int, int]


def initialize(width, height) -> None:
    global test_button

    play_button = Button(width//2, height//2, 200, 200, pygame.Surface((200, 40)))
    help_button = Button(width//2, height//2, 200, 200, pygame.Surface((200, 40)))
    exit_button = Button(width//2, height//2, 200, 200, pygame.Surface((200, 40)))


def draw() -> None:
    window.fill((255,255,255))
    test_button.draw(window)
    

def main(window: pygame.surface.Surface):
    width, height = window.get_size()
    initialize(width, height)

    run, clock = True, pygame.time.Clock()
    while run:
        draw()
        test_button.hand_cursor_active()
        
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