# entidades/proyectil.py
from entidades.base import Entidad

class Proyectil(Entidad):
    def __init__(self, x, y, direccion):
        # Polimorfismo estético: Azul/Cian para el jugador, Amarillo para los aliens
        color = (0, 255, 255) if direccion < 0 else (255, 255, 0)
        
        # Invocamos al constructor de la clase base 'Entidad'
        super().__init__(x, y, color, 4, 15)
        self.velocidad = 7 * direccion  # Dirección negativa sube, positiva baja

    def update(self):
        """Implementación polimórfica del movimiento del proyectil"""
        self.rect.y += self.velocidad
        
        # Si el proyectil sale de los márgenes de la pantalla, se elimina 
        # automáticamente de todos los grupos lógicos y de renderizado.
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()