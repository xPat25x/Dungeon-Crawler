import pygame
import constants

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_type = powerup_type  # 0: speed boost, 1: invincibility, etc.
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, screen_scroll, player):
        # Move powerup along with the screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Handle animation
        animation_cooldown = 150
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.animation_list)
            self.image = self.animation_list[self.frame_index]
            self.update_time = pygame.time.get_ticks()

        # Check collision with the player and apply effect
        if self.rect.colliderect(player.rect):
            if self.powerup_type == 0:
                # Apply a speed boost: multiplier 1.5 for 5000 milliseconds
                player.apply_speed_boost(1.5, 5000)
            # Add additional powerup types here
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect) 