import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # Scaling the Start Button
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # Indicates a bolean value in which the click would be False on default

    def draw(self, surface):
        action = False

        Position = pygame.mouse.get_pos()

        if self.rect.collidepoint(Position): # An If statement that changes the bolean value once the button is clicked 
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
