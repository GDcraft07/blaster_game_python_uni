import random
import pygame
from config import *


def spawn_asteroid():
    if random.random() < STRONG_ASTEROID_CHANCE:
        hp, color = (STRONG_ASTEROID_HP, DARK_RED)

    else:
        hp, color = (ASTEROID_HP, RED)

    return {"hb": pygame.Rect(random.randint(0, WIDTH - ASTEROID_SIZE), -ASTEROID_SIZE, ASTEROID_SIZE, ASTEROID_SIZE), "speed": random.randint(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX), "hp": hp, "color": color}


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ship = pygame.Rect((WIDTH - SHIP_WIDTH) // 2, HEIGHT - (SHIP_HEIGHT + 30), SHIP_WIDTH, SHIP_HEIGHT)
    asteroids = []
    next_spawn = 0
    ballets = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ballets += [pygame.Rect(ship.left, ship.top - BALLET_SIZE, BALLET_SIZE, BALLET_SIZE)]
                ballets += [pygame.Rect(ship.right - BALLET_SIZE, ship.top - BALLET_SIZE, BALLET_SIZE, BALLET_SIZE)]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            ship.x -= SHIP_SPEED
        
        if keys[pygame.K_RIGHT]:
            ship.x += SHIP_SPEED

        if ship.left < 0:
            ship.left = 0
        
        if ship.right > WIDTH:
            ship.right = WIDTH

        now = pygame.time.get_ticks()

        if now >= next_spawn:
            asteroids += [spawn_asteroid()]
            next_spawn = now + random.randint(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)

        for asteroid in asteroids:
            asteroid["hb"].y += asteroid["speed"]
        
        asteroids = [asteroid for asteroid in asteroids if asteroid["hb"].top <= HEIGHT]

        for ballet in ballets:
            ballet.y -= BALLET_SPEED
        
        ballets = [ballet for ballet in ballets if ballet.bottom > 0]

        for ballet in ballets:
            for asteroid in asteroids:
                if ballet.colliderect(asteroid["hb"]):
                    ballets.remove(ballet)
                    asteroid["hp"] -= 1

                    break

        asteroids = [asteroid for asteroid in asteroids if asteroid["hp"] > 0]

        screen.fill(BLACK)

        pygame.draw.rect(screen, GRAY, ship)

        for asteroid in asteroids:
            pygame.draw.rect(screen, asteroid["color"], asteroid["hb"])

        for ballet in ballets:
            pygame.draw.rect(screen, GRAY, ballet)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
