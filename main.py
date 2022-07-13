import pygame
from sys import exit
from random import randint, random
# TO DO:
# Collisions w Asteroids, Music, Sound Effects, Planets (3 = end of game)
# Extra ideas: Game modes - difficulty depending on time, power-ups

# This is the player's class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load("Assets/spaceship.png")
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect(center=(100, 330))
    # Takes Player input and moves spaceship's x-coordinate
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 1
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 1
    # Calls movement and updates the player
    def update(self):
        self.movement()


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global WIDTH
        image = pygame.image.load("Assets/star.png")
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect(center=(randint(10, WIDTH - 15), 0))
        # self.star_rect
    def update(self):
        self.rect.y += 1
        self.destroy()

    def destroy(self):
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global WIDTH
        global HEIGHT
        image = pygame.image.load("Assets/asteroids.png")
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect(center=(randint(15, WIDTH - 15), randint(0, HEIGHT - 100)))
    def update(self):
        self.rect.y += 1
        self.destroy()

    def destroy(self):
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global WIDTH
        global HEIGHT
        image = pygame.image.load("Assets/planet.png")
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect(center=(randint(15, WIDTH - 15), randint(0, HEIGHT - 100)))
    def update(self):
        self.rect.y += 1
        self.destroy()

    def destroy(self):
        if self.rect.bottom > HEIGHT:
            self.rect.y = 0



class GameState():
    def __init__(self):
        self.state = "intro"
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Spaceship())
        self.star_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.planet_group = pygame.sprite.Group()

        # "intro", "main", "reset"
    def intro_game_draw(self):
        spaceship = pygame.image.load("Assets/spaceship.png")
        spaceship = pygame.transform.scale(spaceship, (48, 48))
        spaceship_rect = spaceship.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        intro_game_text = pygame.font.Font(None, 30)
        intro_game_text_render = text = intro_game_text.render('Stars', False, (255, 255, 255))
        intro_game_text_render_rect = intro_game_text_render.get_rect(center=(WIDTH / 2, HEIGHT / 3))

        start_text = pygame.font.Font(None, 25)
        start_text_render = start_text.render("Press Space to Start", False, (255, 255, 255))
        start_text_render_rect = start_text_render.get_rect(center=(WIDTH/2, (HEIGHT/3 + HEIGHT/3)))

        screen.blit(spaceship, spaceship_rect)
        screen.blit(intro_game_text_render, intro_game_text_render_rect)
        screen.blit(start_text_render, start_text_render_rect)

    def main_game_draw(self):
        global screen_type
        global score
        global lives
        for event in pygame.event.get():
            # if event.type == star_timer:
            #     # Limits most overlap
            #     star = Star()
            #     single_star = pygame.sprite.GroupSingle(star)
            #     pygame.sprite.spritecollide(single_star.sprite, self.star_group, True)
            #     self.star_group.add(star)
            star = Star()
            single_star = pygame.sprite.GroupSingle(star)
            pygame.sprite.spritecollide(single_star.sprite, self.star_group, True)
            pygame.sprite.spritecollide(single_star.sprite, self.asteroid_group, True)
            self.star_group.add(star)

            if event.type == planet_timer:
                planet = Planet()
                single_planet = pygame.sprite.GroupSingle(planet)
                pygame.sprite.spritecollide(single_planet.sprite, self.star_group, True)
                pygame.sprite.spritecollide(single_planet.sprite, self.asteroid_group, True)
                pygame.sprite.spritecollide(single_planet.sprite, self.planet_group, True)
                self.planet_group.add(planet)
            if event.type == asteroid_timer:
                asteroid = Asteroid()
                single_asteroid = pygame.sprite.GroupSingle(asteroid)
                pygame.sprite.spritecollide(single_asteroid.sprite, self.asteroid_group, True)
                pygame.sprite.spritecollide(single_asteroid.sprite, self.star_group, True)
                self.asteroid_group.add(single_asteroid)

                star = Star()
                single_star = pygame.sprite.GroupSingle(star)
                pygame.sprite.spritecollide(single_star.sprite, self.star_group, True)
                pygame.sprite.spritecollide(single_star.sprite, self.asteroid_group, True)
                self.star_group.add(star)
        if lives <= 0:
            screen_type = "restart"
        if planets >= 3:
            screen_type = "end"

        self.player.draw(screen)
        self.star_group.draw(screen)
        self.star_group.update()
        self.player.update()
        self.asteroid_group.draw(screen)
        self.planet_group.draw(screen)
        self.planet_group.update()
        self.asteroid_group.update()
        pygame.display.update()

    def restart_game_draw(self):
        global screen_type
        global score
        global lives
        global planets
        asteroid = pygame.image.load("Assets/asteroids.png")
        asteroid = pygame.transform.scale(asteroid, (48, 48))
        asteroid_rect = asteroid.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        restart_game_text = pygame.font.Font(None, 30)
        restart_game_text_render = text = restart_game_text.render('Retry', False, (255, 255, 255))
        restart_game_text_render_rect = restart_game_text_render.get_rect(center=(WIDTH / 2, HEIGHT / 4))


        score_game_text = pygame.font.Font(None, 30)
        score_game_text_render = score_game_text.render('Score: ' + str(score), False, (255, 255, 255))
        score_game_text_render_rect = score_game_text_render.get_rect(center=(WIDTH / 2, HEIGHT / 3))

        start_text = pygame.font.Font(None, 25)
        start_text_render = start_text.render("Press Space to Start", False, (255, 255, 255))
        start_text_render_rect = start_text_render.get_rect(center=(WIDTH / 2, (HEIGHT / 3 + HEIGHT / 3)))

        screen.blit(asteroid, asteroid_rect)
        screen.blit(restart_game_text_render, restart_game_text_render_rect)
        screen.blit(start_text_render, start_text_render_rect)
        screen.blit(score_game_text_render, score_game_text_render_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_type = "main"
                    score = 0
                    lives = 3
                    planets = 0
    def finish_game_draw(self):
        global screen_type
        global score
        planet_img = pygame.image.load("Assets/planet.png")
        planet_img = pygame.transform.scale(planet_img, (48, 48))
        planet_rect = planet_img.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        finish_game_text = pygame.font.Font(None, 18)
        finish_game_text_render = finish_game_text.render("Congrats! You have Finished", False, (255, 255, 255))
        finish_game_text_render_rect = finish_game_text_render.get_rect(center=(WIDTH / 2, HEIGHT / 4))

        score_game_text = pygame.font.Font(None, 30)
        score_game_text_render = score_game_text.render('Score: ' + str(score), False, (255, 255, 255))
        score_game_text_render_rect = score_game_text_render.get_rect(center=(WIDTH / 2, HEIGHT / 3))

        end_text = pygame.font.Font(None, 25)
        end_text_render = end_text.render("Press Space to Quit", False, (255, 255, 255))
        end_text_render_rect = end_text_render.get_rect(center=(WIDTH / 2, (HEIGHT / 3 + HEIGHT / 3)))

        screen.blit(planet_img, planet_rect)
        screen.blit(finish_game_text_render, finish_game_text_render_rect)
        screen.blit(end_text_render, end_text_render_rect)
        screen.blit(score_game_text_render, score_game_text_render_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exit()
                    pygame.quit()


    def collision_sprite(self):
        global score
        global lives
        global planets
        if pygame.sprite.spritecollide(self.player.sprite, self.star_group, True):
            score += 1
        if pygame.sprite.spritecollide(self.player.sprite, self.asteroid_group, True):
            lives -= 1
        if pygame.sprite.spritecollide(self.player.sprite, self.planet_group, True):
            planets += 1
    def display_score(self):
        text_score = pygame.font.Font(None, 20)
        text_score_render = text_score.render("Score: " + str(score), False, (255, 255, 255))
        text_score_rect = text_score_render.get_rect(center=(30, 380))
        screen.blit(text_score_render, text_score_rect)
    def display_lives(self):
        lives_score = pygame.font.Font(None, 20)
        lives_score_render = lives_score.render("Lives: " + str(lives), False, (255, 255, 255))
        lives_score_rect = lives_score_render.get_rect(center=(90, 380))
        screen.blit(lives_score_render, lives_score_rect)
    def display_planets(self):
        planets_score = pygame.font.Font(None, 20)
        planets_score_render = planets_score.render("Planets: " + str(planets), False, (255, 255, 255))
        planets_score_rect = planets_score_render.get_rect(center=(160, 380))
        screen.blit(planets_score_render, planets_score_rect)

    def intro_game(self):
        global screen_type
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_type = "main"
        self.intro_game_draw()
        pygame.display.update()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.main_game_draw()
        self.collision_sprite()
        pygame.display.update()

    def restart_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.restart_game_draw()
        pygame.display.update()

    def finish_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.finish_game_draw()
        pygame.display.update()


# General Setup
pygame.init()
bg_music = pygame.mixer.Sound('Assets/star_music.wav')
bg_music.play(loops=-1)

game_state = GameState()
clock = pygame.time.Clock()
# Screen
pygame.display.set_caption('Stars')
WIDTH = 200
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Timer
star_timer = pygame.USEREVENT + 1
planet_timer = pygame.USEREVENT + 2
asteroid_timer = pygame.USEREVENT + 3
pygame.time.set_timer(star_timer, 100)
pygame.time.set_timer(planet_timer, 5)
pygame.time.set_timer(asteroid_timer, 2)

# Score
score = 0
lives = 3
planets = 0
# Control screen
screen_type = "intro"


while True:
    screen.fill("Black")
    clock.tick(60)
    if screen_type == "intro":
        game_state.intro_game()
    elif screen_type == "main":
        game_state.display_score()
        game_state.display_lives()
        game_state.display_planets()
        game_state.main_game()
    elif screen_type == "restart":
        game_state.restart_game()
    elif screen_type == "end":
        game_state.finish_game()
