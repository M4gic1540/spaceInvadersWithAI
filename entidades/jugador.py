# entidades/jugador.py
import pygame
from entidades.base import Entidad
from entidades.proyectil import Proyectil

class Jugador(Entidad):
    def __init__(self, grupo_proyectiles, grupo_render):
        # Inicializa la base como un rectángulo verde de 50x40 en la posición (400, 550)
        super().__init__(400, 550, (0, 255, 0), 50, 40)
        self.velocidad = 5
        self.grupo_proyectiles = grupo_proyectiles
        self.grupo_render = grupo_render
        self.cooldown = 400  # Milisegundos entre disparos
        self.ultimo_disparo = 0

    def update(self):
        """Implementación polimórfica: Control de movimiento por teclado"""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.velocidad
        if teclas[pygame.K_SPACE]:
            self.disparar()

    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > self.cooldown:
            # Creamos la bala apuntando hacia arriba (-1)
            nueva_bala = Proyectil(self.rect.centerx, self.rect.top, -1)
            
            # La registramos en el grupo de colisiones del jugador y en el render global
            self.grupo_proyectiles.add(nueva_bala)
            self.grupo_render.add(nueva_bala)
            self.ultimo_disparo = tiempo_actual
    
    def activar_tiro_rapido(self):
        """Reduce el tiempo de espera entre disparos (mejora el ataque)"""
        if self.cooldown > 150:  # Ponemos un límite para que no sea injustamente rápido
            self.cooldown -= 80
            print(f"# Cooldown actual: {self.cooldown}ms")
    
    def auto_pilotear(self, lista_aliens):
        """Lógica automatizada para que la nave sirva de Sparring dinámico"""
        if not lista_aliens:
            return

        # 1. Encontrar el alien más cercano horizontalmente
        # (Asegúrate de que 'lista_aliens' sea una lista de Python o un grupo de Pygame)
        alien_objetivo = min(lista_aliens, key=lambda a: abs(a.rect.centerx - self.rect.centerx))
        
        # 2. Persecución horizontal (Alinearse con el objetivo)
        if self.rect.centerx < alien_objetivo.rect.centerx:
            self.rect.x += self.velocidad
        elif self.rect.centerx > alien_objetivo.rect.centerx:
            self.rect.x -= self.velocidad

        # 3. Disparar ráfagas automáticas constantes
        # Nota: Asumo que incrementas esta variable 'frames_desde_ultimo_disparo' en el update del jugador
        if self.frames_desde_ultimo_disparo >= 15:
            self.disparar()
            self.frames_desde_ultimo_disparo = 0