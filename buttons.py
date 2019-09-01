import pygame
pygame.init()

white = (255, 255, 255)
sound = pygame.mixer.Sound("hover.wav")

font = pygame.font.SysFont("comicsansms",30)
def text_obj(text, font):
    text_surf = font.render(text, True, white)
    return text_surf, text_surf.get_rect()

class Button:
    def __init__(self, msg, x, y, width, height, color_active, color_inactive, function = None):
        self.rect_area = pygame.Rect(x, y, width, height)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color_active, self.color_inactive = color_active, color_inactive
        self.function = function
        self.msg = msg

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect_area.collidepoint(mouse):
            pygame.draw.rect(screen, self.color_active, (self.x, self.y, self.width, self.height))
            if click[0] == 1 and self.function != None:
                sound.play()
                self.function()
        else:
            pygame.draw.rect(screen, self.color_inactive, (self.x, self.y, self.width, self.height))

        text = pygame.font.SysFont("comicsansms",15)
        text_surf, text_rect = text_obj(self.msg, text)
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        screen.blit(text_surf, text_rect)
