import pygame
import main_menu
import helper

main_menu_scene: bool = True
helper_scene: bool = False


def main():
    global main_menu_scene, helper_scene
    window = pygame.display.set_mode((1600,900), pygame.FULLSCREEN)
    width, height = window.get_size()
    main_menu.initialize(width, height)
    helper.initialize(width, height)

    run, clock = True, pygame.time.Clock()
    while run:
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        match main_menu.report_activity():
            case "help":
                main_menu_scene = False
                helper_scene = True
            case "quit":
                run = False

        match helper.report_activity():
            case "help_exit":
                main_menu_scene = True
                helper_scene = False

        if main_menu_scene:
            main_menu.update(window)
            main_menu.draw(window)
        if helper_scene:
            helper.update(window)
            helper.draw(window)


if __name__ == '__main__':
    main()
    pygame.quit()