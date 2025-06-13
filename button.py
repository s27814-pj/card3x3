import pygame
from card import Card
GRAY = (127, 127, 127)

class Button():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.rect=pygame.Rect(x, y, width, height)
        self.clicked = False


    def draw(self, surface, card):
        action = False
        if card.is_hidden:
            pygame.draw.rect(surface, GRAY, self.rect)
        else:

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            pygame.draw.rect(surface, card.colour, self.rect)
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(card.N), True, (0, 0, 0))  # Black text
            text_rect = text.get_rect()
            text_rect.center = (self.rect.centerx, self.rect.top + 12)
            surface.blit(text, text_rect)

            text = font.render(str(card.S), True, (0, 0, 0))
            text_rect.center = (self.rect.centerx, self.rect.bottom - 12)
            surface.blit(text, text_rect)

            text = font.render(str(card.W), True, (0, 0, 0))
            text_rect.center = (self.rect.left + 12, self.rect.centery)
            surface.blit(text, text_rect)

            text = font.render(str(card.E), True, (0, 0, 0))
            text_rect.center = (self.rect.right - 12, self.rect.centery)
            surface.blit(text, text_rect)


        return action

    def colour_show(self, surface, colour):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(surface, colour, self.rect)

        return action