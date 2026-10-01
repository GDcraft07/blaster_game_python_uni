import random
import pygame
from config import *


def spawn_asteroid():
    if random.random() < STRONG_ASTEROID_CHANCE:
        hp, color = (STRONG_ASTEROID_HP, DARK_RED)
        kill_score, miss_penalty, hit_penalty = (SCORE_KILL_STRONG, SCORE_MISS_STRONG, SCORE_HIT_STRONG)

    else:
        hp, color = (ASTEROID_HP, RED)
        kill_score, miss_penalty, hit_penalty = (SCORE_KILL_SIMPLE, SCORE_MISS_SIMPLE, SCORE_HIT_SIMPLE)

    return {
        "hb": pygame.Rect(random.randint(0, WIDTH - ASTEROID_SIZE), -ASTEROID_SIZE, ASTEROID_SIZE, ASTEROID_SIZE),
        "y": -ASTEROID_SIZE,
        "speed": random.randint(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX),
        "hp": hp,
        "color": color,
        "kill_score": kill_score,
        "miss_penalty": miss_penalty,
        "hit_penalty": hit_penalty
    }


def spawn_ballet(x, y):
    return {"hb": pygame.Rect(x, y, BALLET_SIZE, BALLET_SIZE), "y": y}


def save_best_score(score, best_score):
    if score > best_score:
        with open(BEST_SCORE_PATH, "w") as file:
            file.write(f"{score}")

        return score

    return best_score


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)
    big_font = pygame.font.Font(None, BIG_FONT_SIZE)

    ship = pygame.Rect((WIDTH - SHIP_WIDTH) // 2, HEIGHT - (SHIP_HEIGHT + 30), SHIP_WIDTH, SHIP_HEIGHT)
    ship_x = float(ship.x)
    asteroids = []
    next_spawn = 0
    ballets = []

    score = 0
    lives = LIVES
    game_over = False
    lives_x = (WIDTH - (LIVES * LIFE_SIZE + (LIVES - 1) * LIFE_GAP)) // 2

    with open(BEST_SCORE_PATH) as file:
        best_score = int(file.read())

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE and not game_over:
                    ballets += [spawn_ballet(ship.left, ship.top - BALLET_SIZE)]
                    ballets += [spawn_ballet(ship.right - BALLET_SIZE, ship.top - BALLET_SIZE)]
                    score -= SCORE_SHOT

        if game_over:
            screen.fill(BLACK)

            title_text = big_font.render("Игра окончена", True, WHITE)
            result_text = font.render(f"Итоговый счёт: {score}", True, WHITE)
            screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 2 - 80))
            screen.blit(result_text, ((WIDTH - result_text.get_width()) // 2, HEIGHT // 2))

            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            ship_x -= SHIP_SPEED * dt

        if keys[pygame.K_RIGHT]:
            ship_x += SHIP_SPEED * dt

        if ship_x < 0:
            ship_x = 0

        if ship_x > WIDTH - SHIP_WIDTH:
            ship_x = WIDTH - SHIP_WIDTH

        ship.x = int(ship_x)

        now = pygame.time.get_ticks()

        if now >= next_spawn:
            asteroids += [spawn_asteroid()]
            next_spawn = now + random.randint(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)

        for asteroid in asteroids:
            asteroid["y"] += asteroid["speed"] * dt
            asteroid["hb"].y = int(asteroid["y"])

        for ballet in ballets:
            ballet["y"] -= BALLET_SPEED * dt
            ballet["hb"].y = int(ballet["y"])

        ballets = [ballet for ballet in ballets if ballet["hb"].bottom > 0]

        for ballet in ballets:
            for asteroid in asteroids:
                if ballet["hb"].colliderect(asteroid["hb"]):
                    ballets.remove(ballet)
                    asteroid["hp"] -= 1

                    break

        alive = []

        for asteroid in asteroids:
            if asteroid["hp"] <= 0:
                score += asteroid["kill_score"]

            elif ship.colliderect(asteroid["hb"]):
                score -= asteroid["hit_penalty"]
                lives -= 1

            elif asteroid["hb"].top > HEIGHT:
                score -= asteroid["miss_penalty"]

            else:
                alive += [asteroid]

        asteroids = alive

        if lives <= 0:
            game_over = True
            best_score = save_best_score(score, best_score)

        screen.fill(BLACK)

        pygame.draw.rect(screen, GRAY, ship)

        for asteroid in asteroids:
            pygame.draw.rect(screen, asteroid["color"], asteroid["hb"])

        for ballet in ballets:
            pygame.draw.rect(screen, GRAY, ballet["hb"])

        for i in range(lives):
            pygame.draw.rect(screen, RED, (lives_x + i * (LIFE_SIZE + LIFE_GAP), 10, LIFE_SIZE, LIFE_SIZE))

        score_text = font.render(f"Счёт: {score}", True, WHITE)
        best_text = font.render(f"Лучший счёт: {best_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 10))

        pygame.display.flip()

    save_best_score(score, best_score)

    pygame.quit()


if __name__ == "__main__":
    main()
