# juego.py
import pygame
import sys
import random
import os
import json  # <-- NUEVO IMPORT: Para serializar matrices de pesos de la IA

# Importaciones de interfaces
from menu import Menu
from pantalla_gameover import PantallaGameOver
from pantalla_victoria import PantallaVictoria

# Importaciones de entidades
from entidades.jugador import Jugador
from entidades.alien import Alien
from entidades.proyectil import Proyectil
from entidades.powerup import PowerUp
from ia.cerebro import CerebroAlien  # <-- Asegurar importación de la entidad IA


class SpaceInvaders:
    def __init__(self):  # <--- A ESTE __init__ ME REFIERO
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Invaders con IA Evolutiva Persistente")
        self.reloj = pygame.time.Clock()

        self.fuente_hud = pygame.font.SysFont("Arial", 20, bold=True)

        self.estado = "MENU"
        self.menu = Menu(self.pantalla)
        self.pantalla_gameover = PantallaGameOver(self.pantalla)
        self.pantalla_victoria = PantallaVictoria(self.pantalla)

        self.frecuencia_disparo_alien = 30

        self.archivo_record = "highscore.txt"
        self.archivo_cerebros = "cerebros_elite.json"

        self.high_score = self.cargar_high_score()
        self.score = 0

        # --- AQUÍ DEJAS EL ORDEN ASÍ ---
        self.generacion = 1  # 1. Primero se crea la variable con valor por defecto
        self.historial_cerebros = (
            self.cargar_banco_genetico()
        )  # 2. Luego se carga el JSON y se sobreescribe el 1 con el número real

        # <-- AQUÍ BORRASTE LA LÍNEA DE self.cargar_numero_generacion()

        self.reiniciar_partida()

    def cargar_high_score(self):
        if os.path.exists(self.archivo_record):
            try:
                with open(self.archivo_record, "r") as archivo:
                    return int(archivo.read().strip())
            except ValueError:
                return 0
        return 0

    def guardar_high_score(self):
        with open(self.archivo_record, "w") as archivo:
            archivo.write(str(self.high_score))

    def cargar_banco_genetico(self):
        """Carga la estructura completa de la IA desde el archivo JSON"""
        if os.path.exists(self.archivo_cerebros):
            try:
                with open(self.archivo_cerebros, "r") as archivo:
                    datos = json.load(archivo)

                    # Verificamos si el formato es el nuevo (diccionario) o el antiguo (lista)
                    if isinstance(datos, dict) and "cerebros" in datos:
                        self.generacion = datos.get("generacion_actual", 1)
                        return [CerebroAlien.deserializar(c) for c in datos["cerebros"]]
                    elif isinstance(datos, list):
                        # Compatibilidad por si tenías un archivo antiguo
                        self.generacion = 1
                        return [CerebroAlien.deserializar(c) for c in datos]
            except (json.JSONDecodeError, KeyError):
                self.generacion = 1
                return []
        self.generacion = 1
        return []

    def cargar_numero_generacion(self):
        """Calcula de forma aproximada en qué generación nos quedamos según los cerebros guardados"""
        if self.historial_cerebros:
            # Si ya hay cerebros, inferimos que al menos estamos avanzados
            return max(1, len(self.historial_cerebros) // 40 + 1)
        return 1

    def guardar_banco_genetico(self):
        """Guarda los top 20 cerebros y el número de generación actual en JSON"""
        self.historial_cerebros.sort(key=lambda c: c.fitness, reverse=True)
        top_cerebros = self.historial_cerebros[:20]

        # Estructuramos un JSON con metadatos
        datos_a_guardar = {
            "generacion_actual": self.generacion,
            "cerebros": [c.serializar() for c in top_cerebros],
        }

        with open(self.archivo_cerebros, "w") as archivo:
            json.dump(datos_a_guardar, archivo, indent=4)

    def reiniciar_partida(self):
        self.score = 0
        self.proyectiles_jugador = pygame.sprite.Group()
        self.proyectiles_enemigos = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.todas_las_entidades = pygame.sprite.Group()

        self.jugador = Jugador(self.proyectiles_jugador, self.todas_las_entidades)
        self.todas_las_entidades.add(self.jugador)

        self.crear_flota_evolutiva()

    def crear_flota_evolutiva(self):
        # 1. Ordenamos el historial completo para identificar el rendimiento
        self.historial_cerebros.sort(key=lambda c: c.fitness, reverse=True)
        
        # 2. SISTEMA DE SELECCIÓN DINÁMICA:
        # En lugar de tomar de una lista infinita, nos aseguramos de que el pool de padres
        # contenga tanto campeones históricos como mutaciones frescas de las últimas rondas.
        # Tomamos un porcentaje un poco más amplio (ej. los 15 mejores) para mantener la diversidad.
        pool_padres = self.historial_cerebros[:15] if len(self.historial_cerebros) >= 15 else self.historial_cerebros

        for fila in range(4):
            if fila == 0:
                color, vida, puntos = (147, 112, 219), 2, 50
            elif fila in (1, 2):
                color, vida, puntos = (240, 230, 140), 1, 20
            else:
                color, vida, puntos = (50, 205, 50), 1, 10

            for columna in range(10):
                cerebro_heredado = None
                if pool_padres:
                    # Selección elitista sesgada: elegimos un padre del pool
                    padre = random.choice(pool_padres)
                    
                    # Dinamismo de mutación: 
                    # El 15% de la flota tendrá mutaciones agresivas (0.3) para descubrir nuevas tácticas,
                    # mientras que el resto mantendrá una herencia más conservadora (0.08).
                    tasa = 0.3 if random.random() < 0.15 else 0.08
                    cerebro_heredado = padre.clonar_con_mutacion(tasa_mutacion=tasa)

                nuevo_alien = Alien(
                    80 + columna * 65,
                    60 + fila * 45,
                    color,
                    vida,
                    puntos,
                    cerebro_previo=cerebro_heredado,
                )
                self.aliens.add(nuevo_alien)
                self.todas_las_entidades.add(nuevo_alien)
        
        # 3. PURGA DE MEMORIA (Crucial):
        # Una vez creada la nueva flota, limpiamos el historial en memoria RAM y nos quedamos
        # solo con la élite real (los 20 mejores). Así evitamos sobrecargar el juego y
        # obligamos al algoritmo a mezclar campeones antiguos con los nuevos que vayan naciendo.
        self.historial_cerebros = self.historial_cerebros[:20]

    def gestionar_enemigos(self):
        self.aliens.update(self.jugador.rect.centerx, self.proyectiles_jugador)

        if self.aliens and random.randint(1, self.frecuencia_disparo_alien) == 1:
            atacante = random.choice(self.aliens.sprites())
            bala_enemiga = Proyectil(atacante.rect.centerx, atacante.rect.bottom, 1)
            self.proyectiles_enemigos.add(bala_enemiga)
            self.todas_las_entidades.add(bala_enemiga)

    def calcular_colisiones(self):
        colisiones_aliens = pygame.sprite.groupcollide(
            self.proyectiles_jugador, self.aliens, True, False
        )
        for b, aliens_impactados in colisiones_aliens.items():
            for alien in aliens_impactados:
                vida_restante = alien.recibir_daño()

                if vida_restante <= 0:
                    cerebro_muerto = alien.calcular_fitness_final()
                    self.historial_cerebros.append(cerebro_muerto)

                    self.aliens.remove(alien)
                    self.todas_las_entidades.remove(alien)

                    self.score += alien.puntos
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.guardar_high_score()

                    if random.randint(1, 100) <= 30:
                        nuevo_upgrade = PowerUp(alien.rect.centerx, alien.rect.centery)
                        self.powerups.add(nuevo_upgrade)
                        self.todas_las_entidades.add(nuevo_upgrade)

        # Recoger items
        impactos_powerups = pygame.sprite.spritecollide(
            self.jugador, self.powerups, True # pyright: ignore[reportArgumentType]
        )
        for powerup in impactos_powerups:
            self.todas_las_entidades.remove(powerup)
            self.score += 50
            if self.score > self.high_score:
                self.high_score = self.score
                self.guardar_high_score()
            self.jugador.activar_tiro_rapido()

        # Condición de Derrota
        if pygame.sprite.spritecollide(self.jugador, self.proyectiles_enemigos, True): # pyright: ignore[reportArgumentType]
            for alien in self.aliens.sprites():
                self.historial_cerebros.append(alien.calcular_fitness_final())

            self.generacion += 1
            self.guardar_banco_genetico()  # <-- GUARDADO EN DISCO DURO INMEDIATO
            self.pantalla_gameover.establecer_score(self.score)
            self.estado = "GAMEOVER"

        # Condición de Victoria
        if not self.aliens:
            self.generacion += 1
            self.guardar_banco_genetico()  # <-- GUARDADO EN DISCO DURO INMEDIATO
            self.pantalla_victoria.establecer_score(self.score)
            self.estado = "VICTORIA"

    def dibujar_hud(self):
        texto_score = self.fuente_hud.render(
            f"SCORE: {self.score}", True, (255, 255, 255)
        )
        texto_high = self.fuente_hud.render(
            f"HI-SCORE: {self.high_score}", True, (212, 175, 55)
        )
        texto_gen = self.fuente_hud.render(
            f"GEN: {self.generacion}", True, (0, 255, 255)
        )

        self.pantalla.blit(texto_score, (20, 15))
        self.pantalla.blit(texto_gen, (360, 15))
        self.pantalla.blit(texto_high, (630, 15))

    def ejecutar(self):
        while True:
            if self.estado == "MENU":
                self.estado = self.menu.verificar_eventos()
                self.menu.dibujar()

            elif self.estado == "GAMEOVER":
                resultado = self.pantalla_gameover.verificar_eventos()
                if resultado == "REINICIAR":
                    self.reiniciar_partida()
                    self.estado = "JUEGO"
                else:
                    self.estado = resultado
                self.pantalla_gameover.dibujar()

            elif self.estado == "VICTORIA":
                resultado = self.pantalla_victoria.verificar_eventos()
                if resultado == "REINICIAR":
                    self.reiniciar_partida()
                    self.estado = "JUEGO"
                else:
                    self.estado = resultado
                self.pantalla_victoria.dibujar()

            elif self.estado == "JUEGO":
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.guardar_banco_genetico()  # Guardar si cierran a la fuerza
                        pygame.quit()
                        sys.exit()

                self.gestionar_enemigos()
                self.jugador.update()
                self.proyectiles_jugador.update()
                self.proyectiles_enemigos.update()
                self.powerups.update()
                self.calcular_colisiones()

                self.pantalla.fill((10, 10, 25))
                self.todas_las_entidades.draw(self.pantalla)
                self.dibujar_hud()

                pygame.display.flip()

            self.reloj.tick(60)
