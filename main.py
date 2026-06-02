# main.py
import pygame
from juego import SpaceInvaders

if __name__ == "__main__":
    # Instanciamos el controlador principal y encendemos el juego
    juego = SpaceInvaders()
    juego.ejecutar()