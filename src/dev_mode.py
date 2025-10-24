import pygame

class Dev:
    def __init__(self) -> None:
        pass

def draw(window: pygame.surface.Surface, width:int, height:int, font: pygame.font.Font):
    window.fill((255,255,255))
    s = 4
    txt = font.render("Dev Mode", 1, (0,0,0))
    pygame.draw.rect(window, (150, 150, 150), (0,0,width,txt.get_height()))
    window.blit(txt, (width*0.1 - txt.get_width()//2,0))
    ...

def main(window: pygame.surface.Surface):
    pygame.font.init()
    font = pygame.font.SysFont("Arial Black", 24)
    width, height = window.get_size()
    
    run, clock = True, pygame.time.Clock()
    while run:
        draw(window, width, height, font)
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