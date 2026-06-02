# pantalla_gameover.py
import pygame
import sys

class PantallaGameOver:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_titulo = pygame.font.SysFont("Impact", 65)
        self.fuente_botones = pygame.font.SysFont("Arial", 25)
        self.fuente_score = pygame.font.SysFont("Arial", 22, bold=True)
        
        self.boton_rect = pygame.Rect(275, 390, 250, 55)
        self.color_boton = (200, 16, 46)
        self.color_texto = (255, 255, 255)
        
        self.score_final = 0

    def establecer_score(self, score):
        """Permite al controlador inyectar el puntaje obtenido al morir"""
        self.score_final = score

    def verificar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.boton_rect.collidepoint(evento.pos):
                        return "REINICIAR"
        return "GAMEOVER"

    def dibujar(self):
        self.pantalla.fill((20, 5, 5))

        # Título
        texto_titulo = self.fuente_titulo.render("GAME OVER", True, (255, 50, 50))
        rect_titulo = texto_titulo.get_rect(center=(400, 160))
        self.pantalla.blit(texto_titulo, rect_titulo)

        # --- NUEVO: Renderizado del puntaje obtenido ---
        texto_puntaje = self.fuente_score.render(f"PUNTUACIÓN FINAL: {self.score_final} PTS", True, (255, 200, 200))
        rect_puntaje = texto_puntaje.get_rect(center=(400, 250))
        self.pantalla.blit(texto_puntaje, rect_puntaje)

        # Botón
        pos_mouse = pygame.mouse.get_pos()
        if self.boton_rect.collidepoint(pos_mouse):
            self.color_boton = (255, 30, 60)
        else:
            self.color_boton = (180, 10, 30)

        pygame.draw.rect(self.pantalla, self.color_boton, self.boton_rect, border_radius=8)
        texto_boton = self.fuente_botones.render("VOLVER A JUGAR", True, self.color_texto)
        rect_texto = texto_boton.get_rect(center=self.boton_rect.center)
        self.pantalla.blit(texto_boton, rect_texto)

        pygame.display.flip()