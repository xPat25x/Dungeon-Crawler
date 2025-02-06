import pygame
import math
import random
import constants

class Weapon():
  def __init__(self, image, arrow_image):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    self.angle = 0
    self.cached_angle = None
    self.cached_image = None
    self.image = pygame.transform.rotate(self.original_image, self.angle)
    self.arrow_image = arrow_image
    self.rect = self.image.get_rect()
    self.fired = False
    self.last_shot = pygame.time.get_ticks()

  def update(self, player):
    shot_cooldown = 50
    arrow = None

    # Adjust mouse position for fullscreen scaling if necessary
    display_size = pygame.display.get_surface().get_size()
    if display_size != (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT):
        scale_factor = min(display_size[0] / constants.SCREEN_WIDTH, display_size[1] / constants.SCREEN_HEIGHT)
        scaled_width = constants.SCREEN_WIDTH * scale_factor
        scaled_height = constants.SCREEN_HEIGHT * scale_factor
        x_offset = (display_size[0] - scaled_width) / 2
        y_offset = (display_size[1] - scaled_height) / 2
        mouse_pos = pygame.mouse.get_pos()
        pos = ((mouse_pos[0] - x_offset) / scale_factor, (mouse_pos[1] - y_offset) / scale_factor)
    else:
        pos = pygame.mouse.get_pos()
    x_dist = pos[0] - player.rect.centerx
    y_dist = -(pos[1] - player.rect.centery)  # -ve because pygame y coordinates increase downwards

    target_angle = math.degrees(math.atan2(y_dist, x_dist))

    # Set bow angle directly for instant response (no smoothing)
    self.angle = target_angle

    # Set the bow's position offset from the player's center
    bow_offset = 2  # Bring the bow even closer to the player
    new_x = player.rect.centerx + bow_offset * math.cos(math.radians(self.angle)) + 12
    new_y = player.rect.centery - bow_offset * math.sin(math.radians(self.angle)) + 10
    self.rect.center = (new_x, new_y)

    # Fire arrow if mouse is pressed and cooldown elapsed
    if pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
      arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
      self.last_shot = pygame.time.get_ticks()

    return arrow

  def draw(self, surface):
    if self.cached_angle != self.angle:
      self.cached_image = pygame.transform.rotate(self.original_image, self.angle)
      self.cached_angle = self.angle
    surface.blit(self.cached_image, ((self.rect.centerx - int(self.cached_image.get_width()/2)), self.rect.centery - int(self.cached_image.get_height()/2)))


class Arrow(pygame.sprite.Sprite):
  def __init__(self, image, x, y, angle):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    self.angle = angle
    self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    #calculate the horizontal and vertical speeds based on the angle
    self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
    self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)#-ve because pygame y coordiate increases down the screen


  def update(self, screen_scroll, obstacle_tiles, enemy_list):
    #reset variables
    damage = 0
    damage_pos = None

    #reposition based on speed
    self.rect.x += screen_scroll[0] + self.dx
    self.rect.y += screen_scroll[1] + self.dy

    #check for collision between arrow and tile walls
    for obstacle in obstacle_tiles:
      if obstacle[1].colliderect(self.rect):
        self.kill()

    #check if arrow has gone off screen
    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
      self.kill()

    #check collision between arrow and enemies
    for enemy in enemy_list:
      if enemy.rect.colliderect(self.rect) and enemy.alive:
        damage = 10 + random.randint(-5, 5)
        damage_pos = enemy.rect
        enemy.health -= damage
        enemy.hit = True
        self.kill()
        break

    return damage, damage_pos

  def draw(self, surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))


class Fireball(pygame.sprite.Sprite):
  def __init__(self, image, x, y, target_x, target_y):
    pygame.sprite.Sprite.__init__(self)
    self.original_image = image
    x_dist = target_x - x
    y_dist = -(target_y - y)
    self.angle = math.degrees(math.atan2(y_dist, x_dist))
    self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    #calculate the horizontal and vertical speeds based on the angle
    self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
    self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)#-ve because pygame y coordiate increases down the screen


  def update(self, screen_scroll, player):
    #reposition based on speed
    self.rect.x += screen_scroll[0] + self.dx
    self.rect.y += screen_scroll[1] + self.dy

    #check if fireball has gone off screen
    if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
      self.kill()

    #check collision between self and player
    if player.rect.colliderect(self.rect) and player.hit == False:
      player.hit = True
      player.last_hit = pygame.time.get_ticks()
      player.health -= 10
      self.kill()


  def draw(self, surface):
    surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
