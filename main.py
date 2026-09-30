import pygame
from config import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ship = pygame.Rect((WIDTH - SHIP_WIDTH) // 2, HEIGHT - (SHIP_HEIGHT + 30), SHIP_WIDTH, SHIP_HEIGHT)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.x -= SHIP_SPEED
        if keys[pygame.K_RIGHT]:
            ship.x += SHIP_SPEED

        if ship.left < 0:
            ship.left = 0
        if ship.right > WIDTH:
            ship.right = WIDTH

        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, ship)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()