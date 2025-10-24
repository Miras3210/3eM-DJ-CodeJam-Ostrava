import pygame

def main(window: pygame.surface.Surface):
    width, height = window.get_size()
    
    run, clock = True, pygame.time.Clock()
    while run:
        window.fill((255,255,255))
        
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
