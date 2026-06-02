# entidades/powerup.py
from entidades.base import Entidad

class PowerUp(Entidad):
    def __init__(self, x, y):
        # Un cuadrado pequeño de color morado/magenta (255, 0, 255)
        super().__init__(x, y, (255, 0, 255), 15, 15)
        self.velocidad = 3

    def update(self):
        """Movimiento vertical descendente autónomo"""
        self.rect.y += self.velocidad
        
        # Auto-destrucción si sale de los límites de la pantalla
        if self.rect.top > 600:
            self.kill()