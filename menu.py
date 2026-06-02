# menu.py
import pygame
import sys


class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.SysFont("Impact", 60)
        self.fuente_botones = pygame.font.SysFont("Arial", 25)

        # Botón JUGAR
        self.boton_jugar = pygame.Rect(300, 200, 200, 55)
        self.color_jugar = (0, 180, 0)

        # Dificultad por defecto
        self.dificultad = "FACIL"

        # Botones de Dificultad
        self.boton_facil = pygame.Rect(230, 380, 150, 45)
        self.boton_dificil = pygame.Rect(420, 380, 150, 45)

    def obtener_dificultad(self):
        """Permite al controlador principal consultar qué dificultad se eligió"""
        return self.dificultad

    def verificar_eventos(self):
        """Maneja los clics en el menú y los botones de dificultad"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    # Si pulsa JUGAR, damos luz verde para iniciar
                    if self.boton_jugar.collidepoint(evento.pos):
                        return "JUEGO"

                    # Si pulsa FÁCIL
                    if self.boton_facil.collidepoint(evento.pos):
                        self.dificultad = "FACIL"

                    # Si pulsa DIFÍCIL
                    if self.boton_dificil.collidepoint(evento.pos):
                        self.dificultad = "DIFICIL"

        return "MENU"

    def dibujar(self):
        self.pantalla.fill((10, 10, 30))

        # 1. Dibujar Título
        texto_titulo = self.fuente_titulo.render("SPACE INVADERS", True, (255, 255, 0))
        rect_titulo = texto_titulo.get_rect(center=(400, 100))
        self.pantalla.blit(texto_titulo, rect_titulo)

        # 2. Efecto Hover en botón JUGAR
        pos_mouse = pygame.mouse.get_pos()
        if self.boton_jugar.collidepoint(pos_mouse):
            self.color_jugar = (0, 255, 0)
        else:
            self.color_jugar = (0, 180, 0)

        pygame.draw.rect(
            self.pantalla, self.color_jugar, self.boton_jugar, border_radius=8
        )
        texto_jugar = self.fuente_botones.render("JUGAR", True, (255, 255, 255))
        rect_jugar = texto_jugar.get_rect(center=self.boton_jugar.center)
        self.pantalla.blit(texto_jugar, rect_jugar)

        # 3. Dibujar Subtítulo de Dificultad
        texto_sub = self.fuente_botones.render(
            "SELECCIONAR DIFICULTAD:", True, (200, 200, 200)
        )
        rect_sub = texto_sub.get_rect(center=(400, 330))
        self.pantalla.blit(texto_sub, rect_sub)

        # 4. Lógica de colores para los botones de dificultad (El activo brilla)
        color_f = (0, 150, 255) if self.dificultad == "FACIL" else (50, 50, 80)
        color_d = (255, 60, 60) if self.dificultad == "DIFICIL" else (80, 50, 50)

        # Dibujar Botón FÁCIL
        pygame.draw.rect(self.pantalla, color_f, self.boton_facil, border_radius=5)
        texto_facil = self.fuente_botones.render("FÁCIL", True, (255, 255, 255))
        rect_facil = texto_facil.get_rect(center=self.boton_facil.center)
        self.pantalla.blit(texto_facil, rect_facil)

        # Dibujar Botón DIFÍCIL
        pygame.draw.rect(self.pantalla, color_d, self.boton_dificil, border_radius=5)
        texto_dificil = self.fuente_botones.render("DIFÍCIL", True, (255, 255, 255))
        rect_dificil = texto_dificil.get_rect(center=self.boton_dificil.center)
        self.pantalla.blit(texto_dificil, rect_dificil)

        pygame.display.flip()
