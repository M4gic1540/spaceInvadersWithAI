# entidades/base.py
import pygame

class Entidad(pygame.sprite.Sprite):
    def __init__(self, x, y, color, ancho, alto):
        super().__init__()
        # Pygame necesita estas dos propiedades de forma obligatoria para sus Grupos
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, *args, **kwargs):
        """
        Método polimórfico. No hace nada aquí, pero será sobrescrito
        por Jugador, Alien y Proyectil con sus comportamientos únicos.
        """
        pass