import random
import pygame
from config import *


def spawn_asteroid():
    if random.random() < BONUS_CHANCE:
        hp, color = (BONUS_HP, YELLOW)
        kill_score, miss_penalty, hit_penalty = (0, 0, 0)
        bonus = random.choice(["life", "rapid"])

    elif random.random() < STRONG_ASTEROID_CHANCE:
        hp, color = (STRONG_ASTEROID_HP, DARK_RED)
        kill_score, miss_penalty, hit_penalty = (SCORE_KILL_STRONG, SCORE_MISS_STRONG, SCORE_HIT_STRONG)
        bonus = None

    else:
        hp, color = (ASTEROID_HP, RED)
        kill_score, miss_penalty, hit_penalty = (SCORE_KILL_SIMPLE, SCORE_MISS_SIMPLE, SCORE_HIT_SIMPLE)
        bonus = None

    return {
        "hb": pygame.Rect(random.randint(0, WIDTH - ASTEROID_SIZE), -ASTEROID_SIZE, ASTEROID_SIZE, ASTEROID_SIZE),
        "y": -ASTEROID_SIZE,
        "speed": random.randint(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX),
        "hp": hp,
        "color": color,
        "kill_score": kill_score,
        "miss_penalty": miss_penalty,
        "hit_penalty": hit_penalty,
        "bonus": bonus
    }


def spawn_ballet(x, y):
    return {"hb": pygame.Rect(x, y, BALLET_SIZE, BALLET_SIZE), "y": y}


def spawn_ballets(ship):
    return [spawn_ballet(ship.left, ship.top - BALLET_SIZE), spawn_ballet(ship.right - BALLET_SIZE, ship.top - BALLET_SIZE)]


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

    stars = [{"x": random.randint(0, WIDTH - STAR_SIZE), "y": random.uniform(0, HEIGHT)} for _ in range(STAR_COUNT)]

    score = 0
    lives = LIVES
    game_over = False
    rapid_time = 0
    shoot_cooldown = 0

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

                if event.key == pygame.K_SPACE and not game_over and rapid_time <= 0:
                    ballets += spawn_ballets(ship)
                    score -= SCORE_SHOT

                if event.key == pygame.K_r and game_over:
                    ship.x = (WIDTH - SHIP_WIDTH) // 2
                    ship_x = float(ship.x)
                    asteroids = []
                    ballets = []
                    next_spawn = 0
                    score = 0
                    lives = LIVES
                    rapid_time = 0
                    shoot_cooldown = 0
                    game_over = False

        if game_over:
            screen.fill(BLACK)

            title_text = big_font.render("Игра окончена", True, WHITE)
            result_text = font.render(f"Итоговый счёт: {score}", True, WHITE)
            hint_text = font.render("R - начать заново", True, WHITE)
            screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 2 - 80))
            screen.blit(result_text, ((WIDTH - result_text.get_width()) // 2, HEIGHT // 2))
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, HEIGHT // 2 + 50))

            pygame.display.flip()
            continue

        rapid_time = max(0, rapid_time - dt)
        shoot_cooldown = max(0, shoot_cooldown - dt)

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

        if rapid_time > 0 and keys[pygame.K_SPACE] and shoot_cooldown <= 0:
            ballets += spawn_ballets(ship)
            shoot_cooldown = RAPID_FIRE_DELAY

        for star in stars:
            star["y"] += STAR_SPEED * dt

            if star["y"] > HEIGHT:
                star["x"] = random.randint(0, WIDTH - STAR_SIZE)
                star["y"] = 0

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

                if asteroid["bonus"] == "life":
                    lives = min(lives + 1, MAX_LIVES)

                elif asteroid["bonus"] == "rapid":
                    rapid_time = BONUS_DURATION

            elif ship.colliderect(asteroid["hb"]):
                score -= asteroid["hit_penalty"]

                if asteroid["bonus"] is None:
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

        for star in stars:
            pygame.draw.rect(screen, WHITE, (star["x"], int(star["y"]), STAR_SIZE, STAR_SIZE))

        pygame.draw.rect(screen, GRAY, ship)

        for asteroid in asteroids:
            pygame.draw.rect(screen, asteroid["color"], asteroid["hb"])

        for ballet in ballets:
            pygame.draw.rect(screen, GRAY, ballet["hb"])

        lives_x = (WIDTH - (lives * LIFE_SIZE + (lives - 1) * LIFE_GAP)) // 2

        for i in range(lives):
            pygame.draw.rect(screen, RED, (lives_x + i * (LIFE_SIZE + LIFE_GAP), 10, LIFE_SIZE, LIFE_SIZE))

        if rapid_time > 0:
            rapid_text = font.render(f"Очередь: {rapid_time:.1f}", True, YELLOW)
            screen.blit(rapid_text, ((WIDTH - rapid_text.get_width()) // 2, 10 + LIFE_SIZE + 8))

        score_text = font.render(f"Счёт: {score}", True, WHITE)
        best_text = font.render(f"Лучший счёт: {best_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(best_text, (WIDTH - best_text.get_width() - 10, 10))

        pygame.display.flip()

    save_best_score(score, best_score)

    pygame.quit()


if __name__ == "__main__":
    main()
