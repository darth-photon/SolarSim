import pygame as pg
import math

pg.init()
WIDTH, HEIGHT = 1400, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Solar system simulator")
clock = pg.time.Clock()

background = pg.image.load('background.jpg')
background = pg.transform.scale(background, (WIDTH, HEIGHT))

class Planets:
    AU  = 149.59e9 # in m
    G   = 6.67408e-11 # in m^3 kg^-1 s^-2
    SCALE = 100 / AU  #1 pixel = 250 m
    dt = 60 * 60 * 24 * 30 # in s
    
    def __init__(self, x_pos: float, y_pos: float, name: str,radius: float, color: tuple, mass: float):
        self.name = name
        self.mass = mass # in kg
        self.radius = radius # in m
        self.color = color
        self.sun = False
        self.distance_to_sun = 0.0
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.orbit = []
        
    def draw(self, screen):
        x = self.x_pos * self.SCALE + WIDTH / 2
        y = self.y_pos * self.SCALE + HEIGHT / 2
        pg.draw.circle(screen, self.color, (x, y), self.radius)
        
    def force(self, other):
        other_x,  other_y = other.x_pos, other.y_pos
        
        # vectors 
        distance_vectors = [other_x - self.x_pos, other_y - self.y_pos]
        distance = math.sqrt(distance_vectors[0]**2 + distance_vectors[1]**2)
        
        if other.sun:
            self.distance_to_sun = distance
            
        force = self.G * self.mass * other.mass / distance**2
        
        # force vectors
        theta = math.atan2(distance_vectors[1], distance_vectors[0])
        force_vectors = [math.cos(theta) * force, math.sin(theta) * force]
        return force_vectors
    
    def update_positions(self, planet_objects):
        total_force = [0, 0]
        for planet in planet_objects.values():
            if planet.name != self.name:
                total_force[0] += self.force(planet)[0]
                total_force[1] += self.force(planet)[1]

        self.x_vel += total_force[0] / self.mass * self.dt
        self.y_vel += total_force[1] / self.mass * self.dt
        
        self.x_pos += self.x_vel * self.dt
        self.y_pos += self.y_vel * self.dt 
        self.orbit.append((self.x_pos, self.y_pos))
        

objects = {"sun":[0, 0, 30, (255,255,0), 1.989e30, 0.0],
                "mercury":[-0.387*Planets.AU, 0, 8, (150,78,150), 3.285e23, 47.4],
                "venus":[0.723*Planets.AU, 0, 10, (255,255,255), 4.867e24, 35.02], 
                "earth":[-1*Planets.AU, 0, 16, (100,149,237), 5.972e24, 29.78], 
                "mars":[-1.524*Planets.AU, 0, 14, (188,39,50), 6.39e23, 24.077],
                "jupiter":[5.203*Planets.AU, 0, 20, (255,165,0), 1.898e27, 13.07], #5.203*Planets.AU
                "saturn":[9.537*Planets.AU, 0, 18, (238,232,170), 5.683e26, 9.69],
                "uranus":[19.191*Planets.AU, 0, 12, (0,255,255), 8.681e25, 6.81],
                "neptune":[30.069*Planets.AU, 0, 12, (0,0,255), 1.024e26, 5.43]}
planet_objects = {}

for name in objects.keys():
    planet_objects[name] = Planets(objects[name][0], objects[name][1] , name, objects[name][2], objects[name][3], objects[name][4])
    planet_objects[name].y_vel = objects[name][5] * 1000
    if name=="sun":
        planet_objects[name].sun = True
    

def main():
    sim = True
    while sim:
        clock.tick(60)
        screen.blit(background, ( 0,0 ) )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sim = False
             
        for pt in planet_objects.keys():
            planet_objects[pt].update_positions(planet_objects)
            planet_objects[pt].draw(screen)
        
        pg.display.update()
        
    pg.quit()
        
main()
