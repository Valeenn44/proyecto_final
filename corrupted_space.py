import pygame 
import os
import time
import random
pygame.font.init()
""""""

ALTO, ANCHO = 690, 690
PANTALLA = pygame.display.set_mode((ALTO, ANCHO))
pygame.display.set_caption("Proyecto Final")

ASSETS_DIR = os.path.join(os.getcwd(), "ASSETS_DIR")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("ASSETS_DIR", "enemigo_verde_2.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("ASSETS_DIR", "enemigo_rosa.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("ASSETS_DIR", "enemigo_verde.png"))

# Jugador ship 
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("ASSETS_DIR", "nave_principal.png"))

# Lasers 
RED_LASER = pygame.image.load(os.path.join("ASSETS_DIR","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("ASSETS_DIR","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("ASSETS_DIR","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("ASSETS_DIR","pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("ASSETS_DIR","FONDO_ESPACIO1.gif")), (ALTO, ANCHO))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None 


class Ship:
    COOLDOWN = 10
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ANCHO):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Jugador(Ship):
    def __init__(self, x, y , health=100):
        super().__init__(x, y , health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ANCHO):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health)/self.max_health, 10))
        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

        
    
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move(self, vel):
        self.y += vel
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 17, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def main():
    run = True
    FPS = 60
    nivel = 0
    vidas = 5
    
    lost = False
    lost_count = 0
    
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 80)
    
    velocidad_jugador = 5
    laser_vel = 4
    
    jugador = Jugador(300, 620)
    
    enemigos = []
    wave_length = 5
    enemy_vel = 2
    
    clock = pygame.time.Clock()
    
    def redraw_window():
        PANTALLA.blit(BG, (0,0))
        # draw text
        N_vidas = main_font.render(f"vidas: {vidas}", 1, (255,255,255))
        N_nivel = main_font.render(f"nivel: {nivel}", 1, (255,255,255))

        PANTALLA.blit(N_vidas, (10, 10))
        PANTALLA.blit(N_nivel, (ALTO - N_nivel.get_width() - 10, 10))

        for enemigo in enemigos:
            enemigo.draw(PANTALLA)

        jugador.draw(PANTALLA)
        
        if lost:
            lost_label = lost_font.render("You lost!!!", 1, (255,255,255))
            PANTALLA.blit(lost_label, (ALTO/2 - lost_label.get_width()/2, 350))

        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()
        
        if vidas <= 0 or jugador.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemigos) == 0:
            nivel += 1
            wave_length += 5
            for i in range(wave_length):
                enemigo = Enemy(random.randrange(50, ALTO - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemigos.append(enemigo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jugador.shoot()
        if keys[pygame.K_w] and jugador.y - velocidad_jugador > 0: # up
            jugador.y -= velocidad_jugador
        if keys[pygame.K_a] and jugador.x - velocidad_jugador > 0: # left
            jugador.x -= velocidad_jugador
        if keys[pygame.K_d] and jugador.x + velocidad_jugador + jugador.get_width() < ALTO: # right
            jugador.x += velocidad_jugador
        if keys[pygame.K_s] and jugador.y + velocidad_jugador + jugador.get_height() + 19 < ANCHO: # down
            jugador.y += velocidad_jugador
        
            
        for enemigo in enemigos[:]: # looping through a copy of list of enemies
            enemigo.move(enemy_vel)
            enemigo.move_lasers(laser_vel, jugador)
            
            if random.randrange(0, 2*60) == 1:
                enemigo.shoot()
            
            if collide(enemigo, jugador):
                jugador.health -= 10
                enemigos.remove(enemigo)
            
            elif enemigo.y + enemigo.get_height() > ANCHO: 
                vidas -= 1
                enemigos.remove(enemigo)
            
                
        jugador.move_lasers(-laser_vel, enemigos)
        
        
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        PANTALLA.blit(BG, (0,0))
        title_label = title_font.render("Click para empezar", 1, (255,255,255))
        PANTALLA.blit(title_label, (ALTO/2 - title_label.get_width()/2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            
    pygame.quit()
if __name__ == "__main__":
    main_menu()