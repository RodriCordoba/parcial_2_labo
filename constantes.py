import pygame
pygame.init()

gravedad = 1
potencia_salto = -10
limite_velocidad_caida = 15
W, H = 1200, 600

velocidad_proyectil = 5
contador_muerte = 0

piso = pygame.Rect(0,0,W,20)

PANTALLA = pygame.display.set_mode((W,H))
def girar_imagenes(lista_original, flip_x: bool, flip_y: bool)-> list:
    lista_girada = []
    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen, flip_x, flip_y))

    return lista_girada

def reescalar_imagen(lista_animaciones, W, H):
    for lista in lista_animaciones:
        for i in range(len(lista)):
            imagen = lista[i]
            lista[i] = pygame.transform.scale(imagen, (W,H))

#FONDOS
UBICACION_FONDO_INICIO = "fondo_inicio.png"
UBICACION_FONDO_PAUSA = "fondo_opciones.png"
UBICACION_FONDO_PERDISTE = "fondo_perdiste.png"
UBICACION_FONDO_RANKING = "fondo_ranking.png"

#BOTONES
UBICACION_BOTON_JUGAR = "botones/jugar.png"
UBICACION_BOTON_PAUSA = "botones/pausa.png"
UBICACION_BOTON_RANKING = "botones/ranking.png"
UBICACION_BOTON_SALIR = "botones/salir.png"
UBICACION_BOTON_GUARDAR = "botones/guardar.png"
UBICACION_BOTON_VOLVER = "botones/volver.png"

#AUDIO 
UBICACION_SONIDO_CLICK = "audio/click.mp3"
UBICACION_SONIDO_INICIAR = "audio/iniciar.mp3"
UBICACION_SONIDO_MUSICA_MENU = "audio/musica_menu.mp3"

#PERSONAJE
personaje_quieto = [
    pygame.image.load("ranger/quieto/4.png"),
    pygame.image.load("ranger/quieto/5.png"),
    pygame.image.load("ranger/quieto/6.png")
]
personaje_camina = [    
    pygame.image.load("ranger/camina/11.png"),
    pygame.image.load("ranger/camina/12.png"),
    pygame.image.load("ranger/camina/13.png"),
    pygame.image.load("ranger/camina/14.png"),
    pygame.image.load("ranger/camina/15.png"),
    pygame.image.load("ranger/camina/16.png")
]
personaje_salta = [    
    pygame.image.load("ranger/salta/46.png"),
    pygame.image.load("ranger/salta/47.png"),
    pygame.image.load("ranger/salta/46.png")
]
ataque_espada = [
    pygame.image.load("ranger/ataque espada/93.png"),
    pygame.image.load("ranger/ataque espada/93.png"),
    pygame.image.load("ranger/ataque espada/92.png")
    ]
personaje_camina_izquierda = girar_imagenes(personaje_camina, True, False)
lista_animaciones = [personaje_quieto, personaje_camina, personaje_camina_izquierda, personaje_salta]
imagenes_reescaladas = reescalar_imagen(lista_animaciones, 30, 70)

#ENEMIGO
enemigo_quieto = [
    pygame.image.load("enemigo_nivel_1/37.png"),
    pygame.image.load("enemigo_nivel_1/34.png"),
    pygame.image.load("enemigo_nivel_1/35.png")
]
enemigo_camina = [
    pygame.image.load("enemigo_nivel_1/12.png"),
    pygame.image.load("enemigo_nivel_1/10.png"),
    pygame.image.load("enemigo_nivel_1/11.png"),
    pygame.image.load("enemigo_nivel_1/7.png"),
    pygame.image.load("enemigo_nivel_1/8.png"),
    pygame.image.load("enemigo_nivel_1/9.png")
]
enemigo_muere = [
    pygame.image.load("enemigo_nivel_1/3.png"),
    pygame.image.load("enemigo_nivel_1/4.png"),
    pygame.image.load("enemigo_nivel_1/5.png"),
    pygame.image.load("enemigo_nivel_1/6.png"),
]
enemigo_camina_izquierda = girar_imagenes(enemigo_camina, True, False)

#BOSS
boss_dispara = [
    pygame.image.load("enemigo/61.png"),
    pygame.image.load("enemigo/62.png"),
    pygame.image.load("enemigo/63.png"),
    pygame.image.load("enemigo/64.png"),
]