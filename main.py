import random
import pygame
from config import *


def spawn_asteroid():
    return pygame.Rect(random.randint(0, WIDTH - ASTEROID_SIZE), -ASTEROID_SIZE, ASTEROID_SIZE, ASTEROID_SIZE)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ship = pygame.Rect((WIDTH - SHIP_WIDTH) // 2, HEIGHT - (SHIP_HEIGHT + 30), SHIP_WIDTH, SHIP_HEIGHT)
    asteroid = spawn_asteroid()

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

        asteroid.y += ASTEROID_SPEED

        if asteroid.top > HEIGHT:
            asteroid = spawn_asteroid()

        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, ship)
        pygame.draw.rect(screen, RED, asteroid)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()