import pygame
import random
import sys
import math

ANCHO, ALTO = 900, 700
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
NEGRO = (10, 10, 10)
GRIS = (50, 50, 50)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("L4D Lite - Hordas Mode")
clock = pygame.time.Clock()
fuente = pygame.font.Font(None, 32)

class Jugador:
    def _init_(self):
        self.rect = pygame.Rect(ANCHO//2, ALTO//2, 35, 35)
        self.vel = 5
        self.vida = 100
        self.max_vida = 100

    def mover(self, keys):
        if keys[pygame.K_w]: self.rect.y -= self.vel
        if keys[pygame.K_s]: self.rect.y += self.vel
        if keys[pygame.K_a]: self.rect.x -= self.vel
        if keys[pygame.K_d]: self.rect.x += self.vel
        self.rect.clamp_ip(pantalla.get_rect())

    def dibujar(self):
        pygame.draw.rect(pantalla, VERDE, self.rect)
        # Barra de vida
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, self.rect.y-10, 35, 5))
        pygame.draw.rect(pantalla, VERDE, (self.rect.x, self.rect.y-10, 35*(self.vida/self.max_vida), 5))

class Zombie:
    def _init_(self, ola):
        lado = random.choice(['top','bottom','left','right'])
        if lado == 'top': x, y = random.randint(0, ANCHO), 0
        elif lado == 'bottom': x, y = random.randint(0, ANCHO), ALTO
        elif lado == 'left': x, y = 0, random.randint(0, ALTO)
        else: x, y = ANCHO, random.randint(0, ALTO)

        self.rect = pygame.Rect(x, y, 30, 30)
        self.vel = 1.5 + ola * 0.3 # Más rápido cada ola
        self.vida = 2 + ola # Más vida cada ola

    def mover(self, jugador):
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.rect.x += dx/dist * self.vel
            self.rect.y += dy/dist * self.vel

    def dibujar(self):
        pygame.draw.rect(pantalla, ROJO, self.rect)

class Bala:
    def _init_(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 8, 8)
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        self.velx = dx/dist * 12
        self.vely = dy/dist * 12

    def mover(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

    def dibujar(self):
        pygame.draw.rect(pantalla, AZUL, self.rect)

def juego():
    jugador = Jugador()
    zombies = []
    balas = []
    ola = 1
    zombies_por_ola = 8
    zombies_spawneados = 0
    zombies_muertos_ola = 0
    cooldown_disparo = 0

    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        jugador.mover(keys)

        # Disparo automático al click
        cooldown_disparo -= 1
        if pygame.mouse.get_pressed()[0] and cooldown_disparo <= 0:
            mx, my = pygame.mouse.get_pos()
            balas.append(Bala(jugador.rect.centerx, jugador.rect.centery, mx, my))
            cooldown_disparo = 8

        # Spawnear horda
        if zombies_spawneados < zombies_por_ola and random.random() < 0.05:
            zombies.append(Zombie(ola))
            zombies_spawneados += 1

        # Nueva ola si matas todos
        if zombies_spawneados == zombies_por_ola and len(zombies) == 0:
            ola += 1
            zombies_por_ola = 8 + ola * 4
            zombies_spawneados = 0
            zombies_muertos_ola = 0
            jugador.vida = min(jugador.max_vida, jugador.vida + 20) # Recompensa

        # Mover y colisiones
        for z in zombies[:]:
            z.mover(jugador)
            if jugador.rect.colliderect(z.rect):
                jugador.vida -= 0.5
                if jugador.vida <= 0:
                    return ola - 1 # Ola en la que moriste

        for b in balas[:]:
            b.mover()
            if not pantalla.get_rect().colliderect(b.rect):
                balas.remove(b)
            for z in zombies[:]:
                if b.rect.colliderect(z.rect):
                    z.vida -= 1
                    balas.remove(b)
                    if z.vida <= 0:
                        zombies.remove(z)
                        zombies_muertos_ola += 1
                    break

        # Dibujar todo
        pantalla.fill(NEGRO)
        # Grid para vibe
        for i in range(0, ANCHO, 50):
            pygame.draw.line(pantalla, GRIS, (i, 0), (i, ALTO))
        for i in range(0, ALTO, 50):
            pygame.draw.line(pantalla, GRIS, (0, i), (ANCHO, i))

        jugador.dibujar()
        for z in zombies: z.dibujar()
        for b in balas: b.dibujar()

        # HUD
        texto_ola = fuente.render(f"OLA: {ola} | Zombies: {len(zombies)}/{zombies_por_ola}", True, BLANCO)
        texto_vida = fuente.render(f"VIDA: {int(jugador.vida)}/100", True, BLANCO)
        pantalla.blit(texto_ola, (10, 10))
        pantalla.blit(texto_vida, (10, 40))

        pygame.display.flip()
        clock.tick(60)

# Loop principal
while True:
    ola_llegada = juego()
    print(f"Moriste en la ola {ola_llegada}. R para revancha")
    esperando = True
    pantalla.fill(NEGRO)
    texto = fuente.render(f"GAME OVER - Llegaste a ola {ola_llegada}. Presiona R", True, ROJO)
    pantalla.blit(texto, (ANCHO//2-200, ALTO//2))
    pygame.display.flip()
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    esperando = False
