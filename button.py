import pygame
import constants

class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def draw(self, surface):
    action = False
    pos = pygame.mouse.get_pos()
    # Adjust mouse position if in fullscreen mode
    if pygame.display.get_surface() and (pygame.display.get_surface().get_flags() & pygame.FULLSCREEN):
        info = pygame.display.Info()
        scale_factor = min(info.current_w / constants.SCREEN_WIDTH, info.current_h / constants.SCREEN_HEIGHT)
        scaled_width = int(constants.SCREEN_WIDTH * scale_factor)
        scaled_height = int(constants.SCREEN_HEIGHT * scale_factor)
        x_offset = (info.current_w - scaled_width) // 2
        y_offset = (info.current_h - scaled_height) // 2
        adjusted_pos = ((pos[0] - x_offset) / scale_factor, (pos[1] - y_offset) / scale_factor)
    else:
        adjusted_pos = pos

    if self.rect.collidepoint(adjusted_pos):
        if pygame.mouse.get_pressed()[0]:
            action = True
    surface.blit(self.image, self.rect)
    return action