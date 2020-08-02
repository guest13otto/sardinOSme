import pygame
from Module_Base import Module
from plot import Plot


def main():
    pygame.init()
    pygame.display.set_caption("ControlGUI(好撚攰")
    screen = pygame.display.set_mode((1080, 720))
    running = True
    clock = pygame.time.Clock()

    plot = Plot(screen, 1080, 720)

    while running:
        plot.update(0, 0.1, -0.2, 0.5, -0.9, 0.75)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)


if __name__ == "__main__":
    main()

