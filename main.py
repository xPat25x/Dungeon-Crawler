#!/usr/bin/env python3
import pygame
from pygame import mixer
import csv
import os
import random
import math
import constants
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button

# ---------------------------
# FUNKSJONER FOR LEVEL DATA
# ---------------------------
def generate_level_data(level):
    if level == 4:
        rows, cols = 20, 20
        data = []
        for r in range(rows):
            data.append([-1] * cols)
        data[rows - 2][cols - 2] = 8
        data[1][1] = 11
        num_monsters = 50
        for i in range(num_monsters):
            x = random.randint(2, cols - 3)
            y = random.randint(2, rows - 3)
            if data[y][x] == -1:
                data[y][x] = random.randint(12, 16)
        return data

    data = []
    for r in range(constants.ROWS):
        data.append([-1] * constants.COLS)
    # Sett utgang og spillstart
    data[constants.ROWS - 2][constants.COLS - 2] = 8
    data[1][1] = 11

    if level < 5:
        num_enemies = level * 2
        for i in range(num_enemies):
            x = random.randint(2, constants.COLS - 3)
            y = random.randint(2, constants.ROWS - 3)
            enemy_tile = random.randint(12, 16)
            data[y][x] = enemy_tile
        if level >= 3:
            data[constants.ROWS // 2][constants.COLS // 2] = 17
    else:
        num_enemies = level * 3
        for i in range(num_enemies):
            x = random.randint(2, constants.COLS - 3)
            y = random.randint(2, constants.ROWS - 3)
            if random.random() < 0.2:
                enemy_tile = random.randint(18, 20)
            else:
                enemy_tile = random.randint(12, 16)
            if data[y][x] == -1:
                data[y][x] = enemy_tile
        mid_row = constants.ROWS // 2
        for col in range(1, constants.COLS - 1, 3):
            data[mid_row][col] = 7
        if level >= 8:
            data[constants.ROWS // 2][constants.COLS // 2] = 17

    return data

def load_level_data(level):
    if level == 4:
        return generate_level_data(level)
    file_path = f"levels/level{level}_data.csv"
    if os.path.exists(file_path):
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            return [[int(tile) for tile in row] for row in reader]
    else:
        return generate_level_data(level)

# ---------------------------
# INITIALISERING AV PYGAME
# ---------------------------
mixer.init()
pygame.init()

info = pygame.display.Info()
full_screen = False
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Lag en virtuell spilloverflate med fast oppløsning
game_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Spilltilstand-variabler
level = 1
game_completed = False
start_game = False
pause_game = False
music_muted = False
start_intro = True
screen_scroll = [0, 0]

# Spillers bevegelsesflagg
moving_left = False
moving_right = False
moving_up = False
moving_down = False
in_shop = False

# ---------------------------
# LAST INN FONT OG BILDER
# ---------------------------
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
small_font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 12)

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# Lyd
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)

# Knapper
start_img = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

# Hjertebilder
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Myntbilder
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

# Potion
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# Våpenbilder
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)

# Flisbilder
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# Karakteranimasjoner
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
animation_types = ["idle", "run"]
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# ---------------------------
# TEKST- OG INFO-FUNKJONER
# ---------------------------
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    game_surface.blit(img, (x, y))

def draw_info():
    pygame.draw.rect(game_surface, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(game_surface, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            game_surface.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and not half_heart_drawn:
            game_surface.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            game_surface.blit(heart_empty, (10 + i * 50, 0))
    draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

def draw_controls():
    controls_text = "F: Fullscreen, C: Shop, ESC: Pause , M: mute/unmute"
    text_surface = font.render(controls_text, True, (200, 200, 200))
    width, height = text_surface.get_size()
    new_width = int(width * 0.6)
    new_surface = pygame.transform.scale(text_surface, (new_width, height))
    game_surface.blit(new_surface, (10, constants.SCREEN_HEIGHT - 30))

# ---------------------------
# FUNKSJONER FOR NIVÅRESETT
# ---------------------------
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)
    return data

def reset_game():
    """Nullstiller spilltilstanden slik at spilleren kan starte på nytt."""
    global level, start_intro, world, player, enemy_list, score_coin, world_data
    global game_completed, pause_game, in_shop, player_start_pos

    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    level = 1
    start_intro = True
    game_completed = False
    pause_game = False
    in_shop = False

    world_data = load_level_data(level)
    world = World()
    world.process_data(world_data, tile_list, item_images, mob_animations)

    temp_score = player.score  # behold eventuelt score
    player = world.player
    player.score = temp_score
    player.alive = True
    enemy_list = world.character_list

    player_start_pos = player.rect.topleft

    score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
    item_group.add(score_coin)
    for item in world.item_list:
        item_group.add(item)

    death_fade.fade_counter = 0

# ---------------------------
# KLASSER FOR SKADETEKST OG FADE
# ---------------------------
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # Full skjerm-fade
            pygame.draw.rect(game_surface, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(game_surface, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(game_surface, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(game_surface, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            if self.fade_counter >= constants.SCREEN_WIDTH:
                fade_complete = True
        elif self.direction == 2:  # Vertikal fade nedover
            pygame.draw.rect(game_surface, self.colour, (0, 0, constants.SCREEN_WIDTH, self.fade_counter))
            if self.fade_counter >= constants.SCREEN_HEIGHT:
                fade_complete = True

        return fade_complete

# ---------------------------
# INITIALISERING AV VERDEN, SPILLER, VÅPEN, ETC.
# ---------------------------
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

# Les inn nivådata (hvis fil finnes) og bygg verden
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

player = world.player
player_start_pos = player.rect.topleft

bow = Weapon(bow_image, arrow_image)
enemy_list = world.character_list

# Sprite-grupper
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)
for item in world.item_list:
    item_group.add(item)

# Skjermfade-effekter
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

# Knapper
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

# ---------------------------
# HOVEDLOOP
# ---------------------------
run = True
while run:
    clock.tick(constants.FPS)

    # Først: sjekk overordnede tilstander
    if not start_game:
        game_surface.fill(constants.MENU_BG)
        if start_button.draw(game_surface):
            start_game = True
            start_intro = True
        if exit_button.draw(game_surface):
            run = False

    elif pause_game:
        game_surface.fill(constants.MENU_BG)
        if resume_button.draw(game_surface):
            pause_game = False
        if exit_button.draw(game_surface):
            run = False

    elif game_completed:
        game_surface.fill(constants.MENU_BG)
        draw_text("You Won the Game!", font, constants.WHITE, constants.SCREEN_WIDTH // 2 - 120, constants.SCREEN_HEIGHT // 2 - 80)
        restart_button.draw(game_surface)

    elif not player.alive:
        # Spilleren er død – vis døds-skjermen med fade-effekt
        game_surface.fill(constants.MENU_BG)
        death_complete = death_fade.fade()
        draw_text("You are dead", font, constants.WHITE, constants.SCREEN_WIDTH // 2 - 80, constants.SCREEN_HEIGHT // 2 - 100)
        if death_complete:
            restart_button.draw(game_surface)

    else:
        # Vanlig spilloppdatering
        game_surface.fill(constants.BG)
        # Spillermovement
        dx = 0
        dy = 0
        if moving_right:
            dx = constants.SPEED
        if moving_left:
            dx = -constants.SPEED
        if moving_up:
            dy = -constants.SPEED
        if moving_down:
            dy = constants.SPEED

        screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)
        for tile in world.obstacle_tiles:
            tile_rect = None
            if isinstance(tile, pygame.Rect):
                tile_rect = tile
            elif isinstance(tile, (list, tuple)) and len(tile) >= 4:
                try:
                    tile_rect = pygame.Rect(int(tile[0]), int(tile[1]), int(tile[2]), int(tile[3]))
                except Exception:
                    continue
            if tile_rect and player.rect.colliderect(tile_rect):
                player.rect.topleft = player_start_pos
                break

        # Oppdater objekter
        world.update(screen_scroll)
        for enemy in enemy_list:
            fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            if enemy.alive:
                enemy.update()
        player.update()
        arrow = bow.update(player)
        if arrow:
            arrow_group.add(arrow)
            shot_fx.play()
        for arrow in arrow_group:
            damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
            if damage:
                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                damage_text_group.add(damage_text)
                hit_fx.play()
        damage_text_group.update()
        fireball_group.update(screen_scroll, player)
        item_group.update(screen_scroll, player, coin_fx, heal_fx)

        # Tegn objekter
        world.draw(game_surface)
        for enemy in enemy_list:
            enemy.draw(game_surface)
        player.draw(game_surface)
        bow.draw(game_surface)
        for arrow in arrow_group:
            arrow.draw(game_surface)
        for fireball in fireball_group:
            fireball.draw(game_surface)
        damage_text_group.draw(game_surface)
        item_group.draw(game_surface)
        draw_info()
        score_coin.draw(game_surface)

        # Navigasjonsindikator for utgangen (stigen)
        if world.exit_tile:
            exit_rect = world.exit_tile[1]
            pygame.draw.circle(game_surface, (255, 255, 0), exit_rect.center, 10, 3)
            draw_text("Ladder", font, (255, 255, 255), exit_rect.centerx - 20, exit_rect.centery - 25)

        # Veiledningspil fra spiller til utgang
        if world.exit_tile and player:
            ladder_center = world.exit_tile[1].center
            player_center = player.rect.center
            dx_arrow = ladder_center[0] - player_center[0]
            dy_arrow = ladder_center[1] - player_center[1]
            angle = math.degrees(math.atan2(-dy_arrow, dx_arrow))
            rotated_arrow = pygame.transform.rotate(arrow_image, angle)
            dist = math.hypot(dx_arrow, dy_arrow)
            if dist != 0:
                norm_dx, norm_dy = dx_arrow/dist, dy_arrow/dist
            else:
                norm_dx, norm_dy = 0, 0
            offset = 40
            arrow_pos = (player_center[0] + norm_dx * offset - rotated_arrow.get_width()//2,
                         player_center[1] + norm_dy * offset - rotated_arrow.get_height()//2)
            game_surface.blit(rotated_arrow, arrow_pos)

        # Sjekk nivå-fullført
        if level_complete:
            if level == 4:
                game_completed = True
            else:
                start_intro = True
                level += 1

                damage_text_group.empty()
                arrow_group.empty()
                item_group.empty()
                fireball_group.empty()

                world_data = load_level_data(level)
                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)

                temp_score = player.score
                player = world.player
                player.score = temp_score

                enemy_list = world.character_list

                score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                item_group.add(score_coin)
                for item in world.item_list:
                    item_group.add(item)

        # Tegn intro-fade ved nivåstart
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # Tegn shop- eller kontroll-overlay
        if in_shop:
            shop_rect = pygame.Rect(100, 50, constants.SCREEN_WIDTH - 200, constants.SCREEN_HEIGHT - 200)
            pygame.draw.rect(game_surface, (0, 0, 0), shop_rect)
            pygame.draw.rect(game_surface, (255, 255, 255), shop_rect, 2)
            draw_text("SHOP", small_font, (255, 255, 255), shop_rect.centerx - 30, shop_rect.top + 20)
            draw_text("Health Upgrade (+20 HP) - Cost: 3 (Press H)", small_font, (255, 255, 255), shop_rect.left + 20, shop_rect.top + 60)
            draw_text("Speed Upgrade (+0.2x) - Cost: 5 (Press S)", small_font, (255, 255, 255), shop_rect.left + 20, shop_rect.top + 100)
            draw_text("Press B to go back", small_font, (255, 255, 255), shop_rect.left + 20, shop_rect.top + 140)
        else:
            draw_controls()

    # ---------------------------
    # EVENT-HANDLING
    # ---------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Håndtering av tastepress
        if event.type == pygame.KEYDOWN:
            if in_shop:
                if event.key == pygame.K_h:
                    if player.score >= 3:
                        player.health += 20
                        player.score -= 3
                elif event.key == pygame.K_s:
                    if player.score >= 5:
                        player.speed_multiplier += 0.2
                        player.score -= 5
                elif event.key == pygame.K_b:
                    in_shop = False
                continue

            if event.key == pygame.K_f:
                full_screen = not full_screen
                try:
                    if full_screen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
                except Exception as e:
                    print("Error toggling fullscreen:", e)
            if event.key == pygame.K_m:
                music_muted = not music_muted
                if music_muted:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(0.3)
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_c:
                in_shop = True
            if event.key == pygame.K_ESCAPE:
                if game_completed:
                    reset_game()
                else:
                    pause_game = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

        # Håndtering av museklikk
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Hvis spillet er vunnet eller spilleren er død, sjekk restart-knappen
            if game_completed or (not player.alive):
                if restart_button.rect.collidepoint(pos):
                    reset_game()

    # Skaleres i fullskjerm-modus
    if full_screen:
        info = pygame.display.Info()
        scale_factor = min(info.current_w / constants.SCREEN_WIDTH, info.current_h / constants.SCREEN_HEIGHT)
        scaled_width = int(constants.SCREEN_WIDTH * scale_factor)
        scaled_height = int(constants.SCREEN_HEIGHT * scale_factor)
        scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
        x_offset = (info.current_w - scaled_width) // 2
        y_offset = (info.current_h - scaled_height) // 2
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, (x_offset, y_offset))
    else:
        screen.blit(game_surface, (0, 0))
    pygame.display.update()

pygame.quit()
