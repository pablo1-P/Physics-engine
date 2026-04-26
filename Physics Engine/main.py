# q spawns rectangles that act as floor and drop to 700 and e is to spawn circles that can bounce off the rectangles and space to clear screen
# first time using pygame wanted to try something that intrests me and physics engines always look cool
# w creates explosion
import pygame
import random


#game start
pygame.init()
window = pygame.display.set_mode((1400,800))
pygame.display.set_caption('Physics Engine')
#class and functions
class Circle():
    def __init__(self, x, y):
        self.color = colors[random.randint(0, len(colors)-1)]
        self.radius = random.randint(10,50)
        self.fill = 0
        self.x = x
        self.y = y
        self.vy = 0.3
        self.circumference = 2*3.14*self.radius
        self.vx = 0
    def gravity(self,object):
            object.y += object.vy
            object.vy += gravity
            object.x += object.vx
            if object.vx > 0:
                object.vx -= 0.4
    def explosion(self, mlocate, force):
        bx, by = self.x, self.y
        ex, ey = mlocate

        dx = bx - ex
        dy = by - ey

        length = (dx*dx + dy*dy) ** 0.5
        if length != 0:
            dx /= length
            dy /= length
    
        self.vx += dx * force
        self.vy += dy * force
    def blackhole (self, mouselocate, strength=5):
        mx, my = mouselocate
    
        dx = mx - self.x
        dy = my - self.y
    

        distance = (dx*dx + dy*dy) ** 0.5
    
        if distance > 0:
            dx /= distance
            dy /= distance
        
            pull_force = strength / (distance * 0.1)
        
            self.vx += dx * pull_force
            self.vy += dy * pull_force
        return distance < 30  






class Rectangle():
    def __init__(self, x, y):
        self.color = (255, 0, 0)
        self.width = 100
        self.height = 50
        self.fill = 0
        self.x = x
        self.y = y
        self.vy = 0.3
        self.xy = (x, y)
    def gravity(self,object):
        if object.y < 700:
            object.y += object.vy
            object.vy += gravity
        elif object.y == 700:
            object.y =  700
        elif object.y > 700:
            object.y = 700


def circle_rect_collision(circle, rect):
    closest_x = max(rect.x, min(circle.x, rect.x + rect.width))
    closest_y = max(rect.y, min(circle.y, rect.y + rect.height))

    dx = circle.x - closest_x
    dy = circle.y - closest_y

    return (dx*dx + dy*dy) < (circle.radius * circle.radius)









#object
circles = [] 
rectangles = [] 
gravity = 0.3
font = pygame.font.SysFont(None, 30)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0), (255, 128, 0), (255, 0, 255)]





#game loop
running = True
while running:
    #60 fps
    pygame.time.delay(16)

    #keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        x_spawn, y_spawn = pygame.mouse.get_pos()
        circles.append(Circle(x_spawn, y_spawn))
    
    if keys[pygame.K_q]:
        x_spawn, y_spawn = pygame.mouse.get_pos()
        rectangles.append(Rectangle(x_spawn, y_spawn))
    #to spawn circle E to spawn rectangle q

    if keys[pygame.K_SPACE]:
        circles.clear()
        rectangles.clear()
    
    if keys[pygame.K_w]:
        mouselocation = pygame.mouse.get_pos()
        for c in circles:
            c.explosion(mouselocation, 10)
    if keys[pygame.K_s]:  
        mouselocation = pygame.mouse.get_pos()
        circles_to_remove = []
        for c in circles:
            if c.blackhole(mouselocation, strength=20):
                circles_to_remove.append(c)



    window.fill((0,0,0))
    for c in circles:
        pygame.draw.circle(window, c.color, (c.x, c.y), c.radius, c.fill)
        c.gravity(c)
        if c.y >= 800:
            c.y = 0
        if c.x <= 100 or c.x >= 1300:
            c.vx = -c.vx

        for r in rectangles:
            if circle_rect_collision(c, r):
                c.vy = -c.vy * 0.7
                c.y = r.y - c.radius


    for r in rectangles:
        pygame.draw.rect(window, r.color, (r.x, r.y, r.width, r.height))
        r.gravity(r)


   
    font = pygame.font.SysFont(None, 30)
    num_of_circ = len(circles)
    num_of_rect = len(rectangles)
    text = f"Circles: {num_of_circ}   Rectangles: {num_of_rect}"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=(10, 10))
    window.blit(text_surface, text_rect)

    #quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update display
    pygame.display.flip()

pygame.quit()