import pygame
import math
import numpy as np
import time

class Circle(object):
    DEFAULT_COL = (255, 0, 0)
    DEFAULT_WIDTH = 0
    def __init__(self, x, y, radius, color=DEFAULT_COL):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen, width=DEFAULT_WIDTH):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, width)

class Polygon(object):
    DEFAULT_COL = (0, 0, 255)
    DEFAULT_WIDTH = 0
    def __init__(self, n, radius=None, color=DEFAULT_COL, origin=(0,0), points=[], width=DEFAULT_WIDTH):
        assert n > 2        # Create an n-sided polygon
        self.n = n
        self.color = color
        self.radius = radius
        self.origin = origin
        self.width = width
        if self.radius is not None:
            self.points = Polygon.calculate_points(n, self.radius, self.origin)
        else:
            self.points = points

    @staticmethod
    def calculate_points(n, radius, origin):
        '''Calculates the co-ordinates (in-relation to an origin) of a regular n-sided polygon.
        This polygon should inscribe a circle centered at the origin with radius = radius'''
        # TODO
        points = []
        # Idea: Convert to polar coordinates, pick the first point as (0, 1)
        theta = 0
        theta_increment = 2 * math.pi / n   # 2pi / n
        for i in range(n):
            x = origin[0] + math.cos(theta) * radius
            y = origin[1] + math.sin(theta) * radius
            points.append((x, y))
            theta += theta_increment
        return points
        

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points, self.width)

    def get_points(self):
        return self.points

class TextBox(object):
    DEFAULT_TEXTCOL = (0, 0, 255)
    DEFAULT_BGCOL = (0, 0, 0)
    def __init__(self, text, x, y, font, color=DEFAULT_TEXTCOL):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.img = font.render(self.text, True, self.color)
        self.rect = self.img.get_rect()
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        

def do_visual_approx(n, screen):
    size = screen.get_size()
    origin = (int(size[0] * 0.28), size[1] // 2)
    DEFAULT_CIRCLE_RADIUS = int(size[1] * 0.28)
    
    unit_circ = Circle(origin[0], origin[1], DEFAULT_CIRCLE_RADIUS)
    
    outer_length = 2 * math.tan(math.pi / n) * (DEFAULT_CIRCLE_RADIUS+1)
    outer_radius = outer_length / (2 * math.sin(math.pi / n))
    outer_poly = Polygon(n, radius=outer_radius, origin=origin, width=0)
    
    inner_poly = Polygon(n, radius=DEFAULT_CIRCLE_RADIUS-1, origin=origin, color=(0, 255, 0), width=1)
    
    outer_poly.draw(screen)
    unit_circ.draw(screen)
    inner_poly.draw(screen)

def write_approx_data(n, screen, font):
    size = screen.get_size()
    box_offset = (size[0]//5 * 3, size[1]//5)

    inner_area = n * math.cos((n-2) * math.pi / (2 * n)) * math.sin((n-2) * math.pi / (2 * n))
    outer_area = n / (math.tan((n-2) * math.pi / (2 * n)))
    display_text1 = "N-gon: {}".format(n)
    display_text2 = "Inner Area: {:.6f}".format(inner_area)
    display_text3 = "Outer Area: {:.6f}".format(outer_area)
    display_text4 = "Circle Area: {:.6f}".format(math.pi)
    inner_err = 100 * abs(math.pi - inner_area) / math.pi
    outer_err = 100 * abs(math.pi - outer_area) / math.pi
    display_text5 = "Relative Errors"
    display_text6 = "Inscribed: {:.3f}%".format(inner_err)
    display_text7 = "Circumscribed: {:.3f}%".format(outer_err)

    DELTA = 45

    text1 = TextBox(display_text1, box_offset[0], box_offset[1], font, color=(255, 255, 255))
    text2 = TextBox(display_text2, box_offset[0], box_offset[1] + 1 * DELTA, font, color=(255, 255, 255))
    text3 = TextBox(display_text3, box_offset[0], box_offset[1] + 2 * DELTA, font, color=(255, 255, 255))
    text4 = TextBox(display_text4, box_offset[0], box_offset[1] + 3 * DELTA, font, color=(255, 255, 255))

    text5 = TextBox(display_text5, box_offset[0], box_offset[1] + 6 * DELTA, font, color=(255, 0, 0))
    text6 = TextBox(display_text6, box_offset[0], box_offset[1] + 7 * DELTA, font, color=(255, 255, 255))
    text7 = TextBox(display_text7, box_offset[0], box_offset[1] + 8 * DELTA, font, color=(255, 255, 255))

    text1.draw(screen)
    text2.draw(screen)
    text3.draw(screen)
    text4.draw(screen)
    text5.draw(screen)
    text6.draw(screen)
    text7.draw(screen)

def main():
    pygame.init()
    pygame.font.init()
    
    FONT_SIZE = 40
    FONT = pygame.font.SysFont(None, FONT_SIZE)
    SCREEN_SIZE = (1080, 720)
    SCREEN_ORIGIN = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("WOW circles")

    screen.fill((0,0,0))
    done = False
    approximation_n = 3
    increase_n = False
    start = time.time()
    increase_delay = 0.3
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
                continue
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    approximation_n = max(approximation_n-1, 3)
                if keys[pygame.K_RIGHT]:
                    approximation_n += 1
                if keys[pygame.K_SPACE]:
                    approximation_n += 10
                if keys[pygame.K_BACKSPACE]:
                    approximation_n = max(approximation_n-10, 3)
                if keys[pygame.K_7]:
                    increase_n = True
                if keys[pygame.K_6]:
                    increase_n = False
                if keys[pygame.K_q]:
                    done = True
                    continue
                
        screen.fill((0,0,0))
        do_visual_approx(approximation_n, screen)
        write_approx_data(approximation_n, screen, FONT)
        if increase_n and (time.time() - start) > increase_delay:
            approximation_n += 1
            start = time.time()
        pygame.display.flip()
    
    print ("Successful exit")

if __name__ == '__main__':
    main()