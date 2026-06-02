import pygame
from entidades.base import Entidad
from ia.cerebro import CerebroAlien  # <-- IMPORTAMOS EL PERCEPTRÓN


class Alien(Entidad):
    def __init__(self, x, y, color, vida, puntos, cerebro_previo=None):
        super().__init__(x, y, color, 40, 30)
        self.color_original = color
        self.vida = vida
        self.puntos = puntos
        self.velocidad = 3  # Agilidad para esquivar

        # Si el algoritmo genético nos pasa un cerebro heredado, lo usamos; si no, nace uno nuevo
        self.cerebro = cerebro_previo if cerebro_previo is not None else CerebroAlien()
        self.frames_vivo = 0
        self.frames_en_borde = 0  # <--- NUEVO: Contador para castigar el estatismo

    def update(self, jugador_x, proyectiles_jugador):
        """Cada fotograma el alien analiza su entorno y decide su destino"""
        self.frames_vivo += 1

        # 1. ENTRADA 1: Distancia horizontal relativa al jugador (normalizada entre -1.0 y 1.0)
        dist_jugador = (jugador_x - self.rect.centerx) / 800.0

        # 2. ENTRADAS 2 y 3: Buscar la bala más cercana en el eje Y que amenace su carril
        bala_cercana_x = 0.0
        bala_cercana_y = 1.0  # 1.0 significa "sin peligro cercano" o bala al fondo
        min_dist_y = 600.0    # Altura estándar de la pantalla de juego

        for bala in proyectiles_jugador:
            # Una bala es una amenaza si está abajo en el eje Y (coordenada menor que el alien) 
            # y subiendo en dirección a su posición actual
            if bala.rect.y < self.rect.y:
                dist_y = self.rect.centery - bala.rect.y
                
                # Monitoreamos un umbral horizontal de advertencia (120 píxeles a la redonda)
                if dist_y < min_dist_y and abs(bala.rect.x - self.rect.centerx) < 120:
                    min_dist_y = dist_y
                    # Desplazamiento horizontal relativo de la bala [-1.0, 1.0]
                    bala_cercana_x = (bala.rect.centerx - self.rect.centerx) / 800.0
                    # Distancia vertical normalizada [0.0 (encima del alien) a 1.0 (lejos)]
                    bala_cercana_y = dist_y / 600.0

        # 3. ENTRADA 4: Posición horizontal relativa a los bordes de la pantalla
        # Mapea el centrox de la pantalla (400) a un rango estable de [-1.0 (borde izq), 1.0 (borde der)]
        dist_borde = (self.rect.centerx - 400.0) / 400.0

        # 4. PROCESAMIENTO AVANZADO: El cerebro MLP toma la decisión matricial
        direccion = self.cerebro.procesar_decision(
            dist_jugador, 
            bala_cercana_x, 
            bala_cercana_y, 
            dist_borde
        )

        # 5. Ejecutar movimiento físico autónomo validando límites de hardware
        self.rect.x += direccion * self.velocidad
        
        # Mantenemos las salvaguardas físicas por si la IA decide forzar los límites
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

        # Descenso pasivo muy lento e individual para simular presión sobre el jugador
        if self.frames_vivo % 120 == 0:
            self.rect.y += 5

        for bala in proyectiles_jugador:
            # CORRECCIÓN: La bala representa una amenaza real si su coordenada Y es MAYOR
            # (está más abajo en la pantalla) que la del alien pero subiendo hacia él.
            if bala.rect.y < self.rect.y:
                dist_y = self.rect.centery - bala.rect.y
                # Si la bala está en un rango de amenaza horizontal cercano (120 píxeles)
                if dist_y < min_dist_y and abs(bala.rect.x - self.rect.centerx) < 120:
                    min_dist_y = dist_y
                    bala_cercana_x = (bala.rect.centerx - self.rect.centerx) / 800.0

        # 3. El cerebro toma la decisión basándose en su matriz de pesos
        direccion = self.cerebro.procesar_decision(dist_jugador, bala_cercana_x, bala_cercana_y, dist_borde)

        # 4. Ejecutar movimiento autónomo validando los límites de la pantalla
        self.rect.x += direccion * self.velocidad

        # DETECTOR DE CAMPING: Si toca los bordes, empezamos a contar frames de castigo
        if self.rect.left <= 0:
            self.rect.left = 0
            self.frames_en_borde += 1
        elif self.rect.right >= 800:
            self.rect.right = 800
            self.frames_en_borde += 1
        else:
            # Si se mantiene en la zona de juego activa, reducimos el castigo acumulado
            if self.frames_en_borde > 0:
                self.frames_en_borde -= 0.5

        # Descenso pasivo muy lento e individual para simular presión sobre el jugador
        if self.frames_vivo % 120 == 0:
            self.rect.y += 5

    def recibir_daño(self):
        self.vida -= 1
        if self.vida > 0:
            self.image.fill(
                (
                    max(0, self.color_original[0] - 100),
                    max(0, self.color_original[1] - 100),
                    max(0, self.color_original[2] - 100),
                )
            )
        return self.vida

    def calcular_fitness_final(self):
        """Asigna la puntuación de supervivencia de este cerebro al morir o ganar"""
        # 1. Base: tiempo de supervivencia + bonus por tipo de fila
        fitness_base = self.frames_vivo + (self.puntos * 5)

        # 2. Penalización por Camping: Restamos de forma exponencial los frames desperdiciados en las paredes
        penalizacion_borde = int(self.frames_en_borde * 2.5)

        # Aplicamos la reducción impidiendo que el fitness caiga por debajo de 1
        self.cerebro.fitness = max(1, fitness_base - penalizacion_borde)
        return self.cerebro
