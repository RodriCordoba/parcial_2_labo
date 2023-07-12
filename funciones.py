import pygame, sys, time
from objetos import *
from constantes import *
from modo import *
from base_de_datos import crear_tablas_db, insertar_jugador, obtener_ranking
pygame.init()

def centrar(imagen):
    return (W // 2) - imagen.get_width() // 2

#FONDOS
fondo_opciones = pygame.image.load(UBICACION_FONDO_PAUSA)
fondo_opciones = pygame.transform.smoothscale(fondo_opciones, (W, H))
fondo_ranking = pygame.image.load(UBICACION_FONDO_RANKING)
fondo_ranking = pygame.transform.smoothscale(fondo_ranking, (W, H))
fondo_perdiste = pygame.image.load(UBICACION_FONDO_PERDISTE)
fondo_perdiste = pygame.transform.smoothscale(fondo_perdiste, (W, H))
fondo_iniciar = pygame.image.load(UBICACION_FONDO_INICIO)
fondo_iniciar = pygame.transform.smoothscale(fondo_iniciar, (W, H))
fondo_ganaste = pygame.image.load(UBICACION_FONDO_GANASTE)
fondo_ganaste = pygame.transform.smoothscale(fondo_ganaste, (W, H))
# IMAGENES DE BOTONES
jugar_imagen = pygame.image.load(UBICACION_BOTON_JUGAR)
pausar_imagen = pygame.image.load(UBICACION_BOTON_PAUSA)
ranking_imagen = pygame.image.load(UBICACION_BOTON_RANKING)
salir_imagen = pygame.image.load(UBICACION_BOTON_SALIR)
volver_imagen = pygame.image.load(UBICACION_BOTON_VOLVER)
guardar_imagen = pygame.image.load(UBICACION_BOTON_GUARDAR)
nivel_1_imagen = pygame.image.load(UBICACION_BOTON_NIVEL_1)
nivel_2_imagen = pygame.image.load(UBICACION_BOTON_NIVEL_2)
nivel_3_imagen = pygame.image.load(UBICACION_BOTON_NIVEL_3)
on_off_volumen_imagen = pygame.image.load(UBICACION_BOTON_ON_OFF_SONIDO)
selector_imagen = pygame.image.load(UBICACION_BOTON_SELECTOR_NIVELES)

#CREACION DE BOTONES
jugar_boton = Boton(jugar_imagen, (140, 50), 120, H-80)
pausar_boton = Boton(pausar_imagen, (120, 40), 30, H-580)
volver_boton = Boton(jugar_imagen, (100, 34), 780, H-80)
jugar_boton_centrado = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, H-220)
jugar_boton_centrado_menu = Boton(jugar_imagen, (100, 34), centrar(jugar_imagen)+10, H-220)
jugar_boton_ganaste = Boton(jugar_imagen, (120, 50), centrar(jugar_imagen)- 200, H-220)
guardar_boton_ganaste = Boton(guardar_imagen, (120, 50), centrar(guardar_imagen), H-220)
salir_boton_ganaste = Boton(salir_imagen, (120, 50), centrar(salir_imagen)+ 200, H-220)
nivel_1_boton = Boton(nivel_1_imagen, (40, 40), centrar(nivel_1_imagen)- 200, H/2)
nivel_2_boton = Boton(nivel_2_imagen, (40, 40), centrar(nivel_2_imagen), H/2)
nivel_3_boton = Boton(nivel_3_imagen, (40, 40), centrar(nivel_3_imagen)+ 200, H/2)
on_off_boton = Boton(on_off_volumen_imagen, (40, 40), 620, H-350)
selector_boton = Boton(selector_imagen, (40, 40), 550, H-350)

jugar_boton_centrado_inicio = Boton(jugar_imagen, (160, 60), 500, H-310)
ranking_boton_inicio = Boton(ranking_imagen, (140, 50), 280, H-305)
salir_boton_inicio = Boton(salir_imagen, (140, 50), 740, H-305)

volver_boton_centrado_opciones = Boton(volver_imagen, (150, 50), 410, H-220)
volver_boton_centrado_niveles = Boton(volver_imagen, (120, 50), centrar(volver_imagen)-219, H-220)
salir_boton_opciones = Boton(salir_imagen, (150, 50), 650, H-220)

jugar_boton_centrado_ranking = Boton(jugar_imagen, (150, 50), 310, H-180)
volver_boton_ranking = Boton(volver_imagen, (150, 50), 650, H-180)

guardar_boton_perdiste = Boton(guardar_imagen, (150, 50), 310, H-220)
salir_boton_perdiste = Boton(salir_imagen, (150, 50), 650, H-220)

def iniciar_juego(volumen = 0.2):
    modo_intro = True
    crear_tablas_db()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)

    while modo_intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_intro = False
                    seleccion_jugar(volumen)
                if evento.key == pygame.K_SPACE:
                    audio_jugar.play()
                    modo_intro = False
                    seleccion_jugar(volumen)
        PANTALLA.blit(fondo, (0, 0))

        if jugar_boton_centrado_inicio.renderizar(PANTALLA):
            audio_jugar.play()
            modo_intro = False
            seleccion_jugar(volumen)
        if ranking_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            ranking()
        if salir_boton_inicio.renderizar(PANTALLA):
            audio_click.play()
            modo_intro = False
            sys.exit()
        pygame.display.update()

def iniciar_bucle_juego_1(volumen):
    bucle_de_juego_nivel_1(volumen)
    return False

def iniciar_bucle_juego_2(volumen):
    bucle_de_juego_nivel_2(volumen)
    return False

def iniciar_bucle_juego_3(volumen):
    bucle_de_juego_nivel_3(volumen)
    return False

def seleccion_jugar(volumen):
    modo_empezar_jugar = True
    audio_jugar = pygame.mixer.Sound(UBICACION_SONIDO_INICIAR)
    audio_nivel_1 = pygame.mixer.Sound(UBICACION_SONIDO_NIVEL_1)
    audio_nivel_2 = pygame.mixer.Sound(UBICACION_SONIDO_NIVEL_2)
    audio_nivel_3 = pygame.mixer.Sound(UBICACION_SONIDO_NIVEL_3)

    while modo_empezar_jugar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_empezar_jugar = False
        PANTALLA.blit(fondo_iniciar, (0, 0))
        if nivel_1_boton.renderizar(PANTALLA):
            audio_jugar.play()
            audio_nivel_1.play()
            modo_empezar_jugar = iniciar_bucle_juego_1(volumen)
            print("ejecutando nivel 1 ")
        if nivel_2_boton.renderizar(PANTALLA):
            audio_jugar.play()
            audio_nivel_2.play()
            modo_empezar_jugar = iniciar_bucle_juego_2(volumen)
            print("ejecutando nivel 2 ")
        if nivel_3_boton.renderizar(PANTALLA):
            audio_jugar.play()
            audio_nivel_3.play()
            modo_empezar_jugar = iniciar_bucle_juego_3(volumen)
            print("ejecutando nivel 3 ")
        if volver_boton_centrado_niveles.renderizar(PANTALLA):
            iniciar_juego(volumen)
        pygame.display.flip()

def mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo, vidas, escudo):
    fuente = pygame.font.SysFont("Arial", 24)
    enemigos_eliminados_texto = fuente.render("Enemigos eliminados: " + str(enemigos_eliminados), True, "Yellow")
    puntuacion_texto = fuente.render("Puntuacion: " + str(puntuacion), True, "Yellow")
    nivel_texto = fuente.render("Nivel: " + str(nivel), True, "Yellow")
    tiempo_texto = fuente.render("Tiempo: " + str(tiempo//1000) + " segundos", True, "Yellow")
    vidas_texto = fuente.render("Vidas: " + str(vidas), True, "Yellow")
    escudo_texto = fuente.render("Escudo: " + str(escudo), True, "Yellow")
    PANTALLA.blit(enemigos_eliminados_texto, (700,H - 585))
    PANTALLA.blit(puntuacion_texto, (700,H - 560))
    PANTALLA.blit(nivel_texto, (1000, H - 585))
    PANTALLA.blit(tiempo_texto, (1000, H - 560))
    PANTALLA.blit(vidas_texto, (500, H - 585))
    PANTALLA.blit(escudo_texto, (500, H - 560))

def ranking(volumen=0.2):
    modo_ranking = True
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    while modo_ranking:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    modo_ranking = False

        PANTALLA.blit(fondo_ranking, (0, 0))
        ranking = obtener_ranking()
        posiciones = [(350, 250), (350, 300), (350, 350)]
        num_elementos = len(ranking)

        for i in range(3):
            if i < num_elementos:
                nombre, puntuacion = ranking[i]
                if i < 3:
                    x, y = posiciones[i]
                    color_fuente = "White" if i == 0 else "Grey"
                    fuente = pygame.font.SysFont("Arial", 36, bold=True)
                    texto_puesto = f"{i+1}. {nombre}"
                    text_puesto = fuente.render(texto_puesto, True, color_fuente)
                    text_puntuacion = fuente.render(str(puntuacion), True, color_fuente)
                    PANTALLA.blit(text_puesto, (x, y))
                    PANTALLA.blit(text_puntuacion, (x + 250, y))

        if jugar_boton_centrado_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            seleccion_jugar(volumen)
        if volver_boton_ranking.renderizar(PANTALLA):
            audio_click.play()
            modo_ranking = False
            iniciar_juego(volumen)
        pygame.display.flip()

def pausa(volume_parametro):
    modo_pausa = True
    volumen = volume_parametro
    tiempo_pausa = 0
    tiempo_inicial_pausa = pygame.time.get_ticks()
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)    
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(volumen)
    esta_arrastrando_mouse = False

    while modo_pausa:
        tiempo_pausa = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_pausa = False
                sys.exit()          
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    posicion_mouse = pygame.mouse.get_pos()
                    if posicion_mouse[0] >= 200 and posicion_mouse[0] <= 700 and posicion_mouse[1] >= 300 and posicion_mouse[1] <= 325:
                        esta_arrastrando_mouse = True
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1: 
                    esta_arrastrando_mouse = False
            elif evento.type == pygame.MOUSEMOTION:
                if esta_arrastrando_mouse:
                    posicion_mouse = pygame.mouse.get_pos()
                    volumen = (posicion_mouse[0] - 300) / 400 # Calcula el volumen con la posición del mouse
                    if volumen < 0.0:
                        volumen = 0.0
                    elif volumen > 1.0:
                        volumen = 1.0
                    pygame.mixer.music.set_volume(volumen)
        PANTALLA.blit(fondo_opciones, (0, 0))

        # Renderizar el deslizador
        pygame.draw.rect(PANTALLA, "Grey", (405, 300, 400, 30))
        posicion_slider = int(volumen * 400) + 405 
        pygame.draw.circle(PANTALLA, "Yellow", (posicion_slider, 314), 16) 
        
        if volver_boton_centrado_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
        if salir_boton_opciones.renderizar(PANTALLA):
            audio_click.play()
            modo_pausa = False
            sys.exit()
        if selector_boton.renderizar(PANTALLA):
            seleccion_jugar(volumen)  
        on_off_boton.on_off_volumen(PANTALLA)
        pygame.display.flip()

        tiempo_actual_pausa = pygame.time.get_ticks()
        tiempo_pausa = tiempo_actual_pausa - tiempo_inicial_pausa
    retorno = {
        "volumen": volumen,
        "tiempo_pausa": tiempo_pausa
    }
    return retorno

def perdiste(puntuacion, volumen):
    modo_perdiste = True
    fuente = pygame.font.SysFont("Arial", 26)
    nombre = ''
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    textbox_rect = pygame.Rect(340, 300, 300,32)

    while modo_perdiste:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_perdiste = False
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 18:
                        nombre += evento.unicode

        PANTALLA.blit(fondo_perdiste, (0, 0))
        pygame.draw.rect(PANTALLA, "White", textbox_rect, 2)

        texto = fuente.render(nombre, True, "White")
        ingresar_nombre_texto = fuente.render("Ingresar nombre:", True, "White")
        PANTALLA.blit(ingresar_nombre_texto, (textbox_rect.x, textbox_rect.y - 30))
        PANTALLA.blit(texto, (textbox_rect.x +5, textbox_rect.y + 5))

        if guardar_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_perdiste = False
            insertar_jugador(nombre, puntuacion)
            ranking(volumen)
        if salir_boton_perdiste.renderizar(PANTALLA):
            audio_click.play()
            modo_perdiste = False
            sys.exit()
        pygame.display.flip()

def ganaste(puntuacion, volumen):
    modo_ganaste = True
    fuente = pygame.font.SysFont("Arial", 26)
    nombre = ''
    audio_click = pygame.mixer.Sound(UBICACION_SONIDO_CLICK)

    textbox_rect = pygame.Rect(340, 300, 300, 32)

    while modo_ganaste:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                modo_ganaste = False
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 18:
                        nombre += evento.unicode

        PANTALLA.blit(fondo_ganaste, (0, 0))
        pygame.draw.rect(PANTALLA, "White", textbox_rect, 2)

        texto = fuente.render(nombre, True, "White")
        ingresar_nombre_texto = fuente.render("Ingresar nombre:", True, "White")
        PANTALLA.blit(ingresar_nombre_texto, (textbox_rect.x, textbox_rect.y - 30))
        PANTALLA.blit(texto, (textbox_rect.x + 5, textbox_rect.y + 5))

        if guardar_boton_ganaste.renderizar(PANTALLA):
            audio_click.play()
            modo_ganaste = False
            insertar_jugador(nombre, puntuacion)
            ranking(volumen)
        if salir_boton_ganaste.renderizar(PANTALLA):
            audio_click.play()
            modo_ganaste = False
            sys.exit()
        if jugar_boton_ganaste.renderizar(PANTALLA):
            audio_click.play()
            seleccion_jugar(volumen)
        pygame.display.flip()

def aplicar_gravedad(pantalla, personaje, pisos, plataformas):
    if personaje.esta_saltando:
        animar_personaje(pantalla, personaje.lados["main"], personaje_salta, personaje)
        personaje.desplazamiento_y += gravedad
    else:
        colision_piso = False
        for piso in pisos:
            if personaje.lados["bottom"].colliderect(piso["main"]):
                colision_piso = True
                personaje.rect.bottom = piso["main"].top + 1
                break
        if not colision_piso:
            personaje.desplazamiento_y += gravedad 
        plataforma_colisionada = pygame.sprite.spritecollideany(personaje, plataformas)
        if plataforma_colisionada:
            if personaje.rect.bottom <= plataforma_colisionada.rect.centery:
                personaje.rect.bottom = plataforma_colisionada.rect.top + 1
                personaje.esta_saltando = False
                personaje.desplazamiento_y = 0
    personaje.rect.y += personaje.desplazamiento_y

def mover(rectangulo: pygame.rect, velocidad):
    for lado in rectangulo:
        rectangulo[lado].x += velocidad

def animar_personaje(pantalla, rectangulo, accion, personaje):
    largo = len(accion)
    if personaje.contador_pasos >= largo:
        personaje.contador_pasos = 0

    pantalla.blit(accion[personaje.contador_pasos], rectangulo)
    personaje.contador_pasos += 1

def actualizar_pantalla(pantalla, lados_piso, grupo_enemigos, grupo_plataformas, orbe, personaje):
    pantalla.blit(fondo, (0,0))
    for plataforma in grupo_plataformas:
        pantalla.blit(plataforma.image, plataforma.rect)
    pantalla.blit(orbe.image, orbe.rect)
    match personaje.que_hace:
        case "Derecha":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], personaje_camina, personaje)
            mover(personaje.lados, personaje.velocidad)
        case "Izquierda":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], personaje_camina_izquierda, personaje)
            mover(personaje.lados, personaje.velocidad*-1)
        case "Salta":
            if not personaje.esta_saltando:
                personaje.esta_saltando = True
                personaje.desplazamiento_y = potencia_salto
        case "Quieto":
            if not personaje.esta_saltando:
                if personaje.direccion == "derecha":
                    animar_personaje(pantalla, personaje.lados["main"], personaje_quieto, personaje)
                else:
                    animar_personaje(pantalla, personaje.lados["main"], personaje_quieto_izquierda, personaje)
        case "Ataque_derecha":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], ataque_espada, personaje)
        case "Ataque_izquierda":
            if not personaje.esta_saltando:
                rectangulo_copia = personaje.lados['main'].copy()
                rectangulo_copia.x -= 45
                animar_personaje(pantalla, rectangulo_copia, ataque_espada_izquierda, personaje)
    for enemigo in grupo_enemigos:
        match enemigo.que_hace:
            case "derecha":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_camina, enemigo)
            case "izquierda":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_camina_izquierda, enemigo)
            case "quieto":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_quieto, enemigo)
        enemigo.update(grupo_plataformas)
    aplicar_gravedad(PANTALLA, personaje, lados_piso, grupo_plataformas)
def actualizar_pantalla_boss(pantalla, lados_piso, grupo_enemigos, grupo_plataformas, orbe, personaje, boss):
    pantalla.blit(fondo, (0,0))
    for plataforma in grupo_plataformas:
        pantalla.blit(plataforma.image, plataforma.rect)
    pantalla.blit(orbe.image, orbe.rect)
    pantalla.blit(boss.imagen, boss.rect)
    match personaje.que_hace:
        case "Derecha":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], personaje_camina, personaje)
            mover(personaje.lados, personaje.velocidad)
        case "Izquierda":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], personaje_camina_izquierda, personaje)
            mover(personaje.lados, personaje.velocidad*-1)
        case "Salta":
            if not personaje.esta_saltando:
                personaje.esta_saltando = True
                personaje.desplazamiento_y = potencia_salto
        case "Quieto":
            if not personaje.esta_saltando:
                if personaje.direccion == "derecha":
                    animar_personaje(pantalla, personaje.lados["main"], personaje_quieto, personaje)
                else:
                    animar_personaje(pantalla, personaje.lados["main"], personaje_quieto_izquierda, personaje)
        case "Ataque_derecha":
            if not personaje.esta_saltando:
                animar_personaje(pantalla, personaje.lados["main"], ataque_espada, personaje)
        case "Ataque_izquierda":
            if not personaje.esta_saltando:
                rectangulo_copia = personaje.lados['main'].copy()
                rectangulo_copia.x -= 45
                animar_personaje(pantalla, rectangulo_copia, ataque_espada_izquierda, personaje)
    for enemigo in grupo_enemigos:
        match enemigo.que_hace:
            case "derecha":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_camina, enemigo)
            case "izquierda":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_camina_izquierda, enemigo)
            case "quieto":
                animar_personaje(pantalla, enemigo.lados["main"], enemigo_quieto, enemigo)
        enemigo.update(grupo_plataformas)
    aplicar_gravedad(PANTALLA, personaje, lados_piso, grupo_plataformas)

def animar_muerte_enemigo(pantalla, enemigo_muere, rectangulo_enemigo): 
    global contador_muerte
    largo = len(enemigo_muere)
    if contador_muerte >= largo:
        return
    pantalla.blit(enemigo_muere[contador_muerte], rectangulo_enemigo)
    contador_muerte += 1
    pygame.display.flip()
    pygame.time.delay(100)

def eliminar_enemigo(enemigo):
    enemigo.x = -1000
    enemigo.y = -1000

def bucle_de_juego_nivel_1(volumen_parametro = 0.2):
    #MUSICA
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    volumen = volumen_parametro
    pygame.mixer.music.set_volume(volumen)
    sonido_muere_personaje = pygame.mixer.Sound(UBICACION_SONIDO_RANGER_MUERE)
    sonido_muere_enemigo = pygame.mixer.Sound(UBICACION_SONIDO_ENEMIGO_MUERE)
    #TEXTO
    fuente = pygame.font.SysFont("Arial", 100)
    perdiste_texto = fuente.render("Perdiste!", 0, "Red")
    #FONDO
    fondo = pygame.image.load("fondos/fondo_ciudad.jpg")
    fondo = pygame.transform.scale(fondo, (W,H))
    #FPS
    FPS = 15
    RELOJ = pygame.time.Clock()
    tick = pygame.USEREVENT + 0
    pygame.time.set_timer(tick, 100)
    #PERSONAJE
    personaje = Personaje(H/2 -250, 450, personaje_quieto)
    #PLATAFORMAS
    piso.top = personaje.rect.bottom
    lados_piso = obtener_rectangulos(piso)
    plataforma_1 = Plataforma(380, 460, ("fondos/13.png"))
    plataforma_2 = Plataforma(1000, 460, ("fondos/14.png"))
    lados_plataforma = obtener_rectangulos(plataforma_1.rect)
    lados_plataforma_2 = obtener_rectangulos(plataforma_2.rect)
    lista_plataformas = [lados_piso, lados_plataforma, lados_plataforma_2]
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(plataforma_1, plataforma_2)
    #ENEMIGO
    grupo_enemigos = Enemigo.generar_enemigos(2)
    #ESPADA
    espada = Espada(H/2 -230, 430, 40)
    rectangulo_espada = pygame.Rect(espada.x,espada.y,espada.z,espada.z)
    rectangulo_espada_izquierda = pygame.Rect(espada.x, espada.y,espada.z,espada.z)
    lados_espada = obtener_rectangulos(rectangulo_espada)
    lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
    #ORBE
    orbe = Orbe(H/2 -250, 390)
    grupo_orbes = pygame.sprite.Group()
    grupo_orbes.add(orbe)
    #PUNTUACION 
    enemigos_eliminados = 0
    nivel = 1
    puntuacion = 0
    tiempo = 180000
    juego_corriendo = True
    vidas = 3
    tiempo_colision = 0

    while juego_corriendo:
        milisegundos = RELOJ.tick(FPS)
        tiempo -= milisegundos
        if tiempo < 1:
            PANTALLA.blit(fondo_perdiste, (0,0))
            PANTALLA.blit(perdiste_texto, (450, 250))
            pygame.display.flip()
            time.sleep(2)
            perdiste(puntuacion, volumen)
        #EVENTOS 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_corriendo = False
                sys.exit(0)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    retorno = pausa(volumen)
                    volumen = retorno['volumen']
                if evento.key == pygame.K_TAB:
                    cambiar_modo()

        personaje.update()
        rectangulo_espada.x = personaje.rect.x +45
        rectangulo_espada.y = personaje.rect.y 
        rectangulo_espada_izquierda.x = personaje.rect.x -45
        rectangulo_espada_izquierda.y = personaje.rect.y 
        lados_espada = obtener_rectangulos(rectangulo_espada)
        lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
        personaje.esta_saltando = False
        orbe.update()

        if personaje.lados["main"].colliderect(orbe.rect):
            personaje.tiene_escudo = True
            eliminar_enemigo(orbe.lados['main'])
            print("escudo")
            puntuacion += 20

        grupo_plataformas.update()
        grupo_plataformas.draw(PANTALLA)

        for enemigo in grupo_enemigos:
            if personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == False and vidas == 0:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700: 
                    sonido_muere_personaje.play()
                    print("Personaje eliminado!")
                    PANTALLA.blit(fondo_perdiste, (0,0))
                    PANTALLA.blit(perdiste_texto, (450, 250))
                    pygame.display.flip()
                    time.sleep(2)
                    perdiste(puntuacion, volumen)
            elif personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == True:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    print("ataque bloqueado")
                    personaje.tiene_escudo = False
                    tiempo_colision = 0 
            elif personaje.lados['main'].colliderect(enemigo.lados['main']) and personaje.tiene_escudo == False:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    vidas -= 1
                    tiempo_colision = 0
            elif (personaje.que_hace == "Ataque_derecha" and enemigo.lados["main"].colliderect(rectangulo_espada))or(personaje.que_hace == "Ataque_izquierda" and enemigo.lados["main"].colliderect(rectangulo_espada_izquierda)):
                sonido_muere_enemigo.play()
                animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados["main"])
                eliminar_enemigo(enemigo.lados["main"])
                print("Enemigo eliminado por ataque de espada!")
                grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                puntuacion += 50
                enemigos_eliminados += 1
                if vidas < 3:
                    vidas += 1
            enemigo.update(grupo_plataformas)
            tiempo_anterior = pygame.time.get_ticks()
        if enemigos_eliminados > 3:
            ganaste(puntuacion, volumen)

        actualizar_pantalla(PANTALLA, lista_plataformas, grupo_enemigos, grupo_plataformas, orbe, personaje)
        for proyectil in proyectiles_juego_personaje:
            proyectil.update()
            PANTALLA.blit(proyectil.imagen, proyectil.rect)

            for enemigo in grupo_enemigos:
                if proyectil.rect.colliderect(enemigo.rect):
                    sonido_muere_enemigo.play()
                    animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados['main'])
                    eliminar_enemigo(enemigo.lados['main'])
                    grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                    proyectil.kill()
                    puntuacion += 70
                    enemigos_eliminados += 1

        if get_mode():
            for lado in personaje.lados:
                pygame.draw.rect(PANTALLA, "Blue", personaje.lados[lado], 2)

            for lado in lados_espada:
                pygame.draw.rect(PANTALLA, "Red", lados_espada[lado], 2)
            for lado in lados_espada_izquierda:
                pygame.draw.rect(PANTALLA, "Red", lados_espada_izquierda[lado], 2)

            for lado in lados_piso:
                pygame.draw.rect(PANTALLA, "Green", lados_piso[lado], 2)

            for lado in lados_plataforma:
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_2[lado], 2)

            for enemigo in grupo_enemigos:
                for lado in enemigo.lados:
                    pygame.draw.rect(PANTALLA, "Cyan", enemigo.lados[lado], 2)

        #BOTON PAUSA
        if pausar_boton.renderizar(PANTALLA):
            retorno = pausa(volumen)
            volumen = retorno['volumen']
            tiempo -= retorno['tiempo_pausa']     
        mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo, vidas, personaje.tiene_escudo)
        pygame.display.flip()

def bucle_de_juego_nivel_2(volumen_parametro = 0.2):
    #MUSICA
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    volumen = volumen_parametro
    sonido_muere_personaje = pygame.mixer.Sound(UBICACION_SONIDO_RANGER_MUERE)
    sonido_muere_enemigo = pygame.mixer.Sound(UBICACION_SONIDO_ENEMIGO_MUERE)
    pygame.mixer.music.set_volume(volumen)
    #TEXTO
    fuente = pygame.font.SysFont("Arial", 100)
    perdiste_texto = fuente.render("Perdiste!", 0, "Red")
    #FONDO
    fondo = pygame.image.load("fondos/fondo_ciudad.jpg")
    fondo = pygame.transform.scale(fondo, (W,H))
    #FPS
    FPS = 15
    RELOJ = pygame.time.Clock()
    tick = pygame.USEREVENT + 0
    pygame.time.set_timer(tick, 100)
    #PERSONAJE
    personaje = Personaje(H/2 -250, 450, personaje_quieto)
    #PLATAFORMAS
    piso.top = personaje.rect.bottom
    lados_piso = obtener_rectangulos(piso)
    plataforma_1 = Plataforma(250, 460, ("fondos/13.png"))
    plataforma_2 = Plataforma(365, 460, ("fondos/7.png"))
    plataforma_3 = Plataforma(365, 400, ("fondos/14.png"))
    plataforma_4 = Plataforma(480, 400, ("fondos/14.png"))
    plataforma_5 = Plataforma(480, 460, ("fondos/7.png"))
    plataforma_6 = Plataforma(595, 460, ("fondos/7.png"))
    plataforma_7 = Plataforma(595, 400, ("fondos/7.png"))
    plataforma_8 = Plataforma(595, 340, ("fondos/7.png"))
    plataforma_9 = Plataforma(710, 400, ("fondos/7.png"))
    plataforma_10 = Plataforma(710, 460, ("fondos/7.png"))
    plataforma_11 = Plataforma(825, 460, ("fondos/13.png"))
    lados_plataforma = obtener_rectangulos(plataforma_1.rect)
    lados_plataforma_2 = obtener_rectangulos(plataforma_2.rect)
    lados_plataforma_3 = obtener_rectangulos(plataforma_3.rect)
    lados_plataforma_4 = obtener_rectangulos(plataforma_4.rect)
    lados_plataforma_5 = obtener_rectangulos(plataforma_5.rect)
    lados_plataforma_6 = obtener_rectangulos(plataforma_6.rect)
    lados_plataforma_7 = obtener_rectangulos(plataforma_7.rect)
    lados_plataforma_8 = obtener_rectangulos(plataforma_8.rect)
    lados_plataforma_9 = obtener_rectangulos(plataforma_9.rect)
    lados_plataforma_10 = obtener_rectangulos(plataforma_10.rect)
    lados_plataforma_11 = obtener_rectangulos(plataforma_11.rect)
    lista_plataformas = [lados_piso, lados_plataforma, lados_plataforma_2, lados_plataforma_3, lados_plataforma_4, lados_plataforma_5, lados_plataforma_6, lados_plataforma_7, lados_plataforma_8, lados_plataforma_9, lados_plataforma_10, lados_plataforma_11]
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(plataforma_1, plataforma_2, plataforma_3, plataforma_4, plataforma_5, plataforma_6, plataforma_7, plataforma_8, plataforma_9, plataforma_10, plataforma_11)
    #ENEMIGO
    grupo_enemigos = Enemigo.generar_enemigos(5)
    #ESPADA
    espada = Espada(H/2 -230, 430, 40)
    rectangulo_espada = pygame.Rect(espada.x,espada.y,espada.z,espada.z)
    rectangulo_espada_izquierda = pygame.Rect(espada.x, espada.y,espada.z,espada.z)
    lados_espada = obtener_rectangulos(rectangulo_espada)
    lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
    #ORBE
    orbe = Orbe(620, 200)
    grupo_orbes = pygame.sprite.Group()
    grupo_orbes.add(orbe)
    #PUNTUACION 
    enemigos_eliminados = 0
    nivel = 2
    puntuacion = 0
    tiempo = 180000
    juego_corriendo = True
    vidas = 3
    tiempo_colision = 0

    while juego_corriendo:
        milisegundos = RELOJ.tick(FPS)
        tiempo -= milisegundos
        if tiempo < 0:
            sonido_muere_personaje.play()
            PANTALLA.blit(fondo_perdiste, (0,0))
            PANTALLA.blit(perdiste_texto, (450, 250))
            sonido_muere_personaje.play()
            pygame.display.flip()
            time.sleep(2)
            perdiste(puntuacion, volumen)
        #EVENTOS 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_corriendo = False
                sys.exit(0)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    retorno = pausa(volumen)
                    volumen = retorno['volumen']
                if evento.key == pygame.K_TAB:
                    cambiar_modo()

        personaje.update()
        rectangulo_espada.x = personaje.rect.x +45
        rectangulo_espada.y = personaje.rect.y
        rectangulo_espada_izquierda.x = personaje.rect.x -45
        rectangulo_espada_izquierda.y = personaje.rect.y 
        lados_espada = obtener_rectangulos(rectangulo_espada)
        lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
        personaje.esta_saltando = False
        orbe.update()

        if personaje.lados["main"].colliderect(orbe.rect):
            personaje.tiene_escudo = True
            eliminar_enemigo(orbe.lados['main'])
            print("escudo")
            puntuacion += 20

        grupo_plataformas.update()
        grupo_plataformas.draw(PANTALLA)

        for enemigo in grupo_enemigos:
            if personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == False and vidas == 0:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700: 
                    sonido_muere_personaje.play()
                    print("Personaje eliminado!")
                    PANTALLA.blit(fondo_perdiste, (0,0))
                    PANTALLA.blit(perdiste_texto, (450, 250))
                    pygame.display.flip()
                    time.sleep(2)
                    perdiste(puntuacion, volumen)
            elif personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == True:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    print("ataque bloqueado")
                    personaje.tiene_escudo = False
                    tiempo_colision = 0 
            elif personaje.lados['main'].colliderect(enemigo.lados['main']) and personaje.tiene_escudo == False:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    vidas -= 1
                    tiempo_colision = 0
            elif (personaje.que_hace == "Ataque_derecha" and enemigo.lados["main"].colliderect(rectangulo_espada))or(personaje.que_hace == "Ataque_izquierda" and enemigo.lados["main"].colliderect(rectangulo_espada_izquierda)):
                sonido_muere_enemigo.play()
                animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados["main"])
                eliminar_enemigo(enemigo.lados["main"])
                print("Enemigo eliminado por ataque de espada!")
                grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                puntuacion += 50
                enemigos_eliminados += 1
                if vidas < 3:
                    vidas += 1
            enemigo.update(grupo_plataformas)
            tiempo_anterior = pygame.time.get_ticks()
        if enemigos_eliminados > 6:
            ganaste(puntuacion, volumen)

        actualizar_pantalla(PANTALLA, lista_plataformas, grupo_enemigos, grupo_plataformas, orbe, personaje)

        for proyectil in proyectiles_juego_personaje:
            proyectil.update()
            PANTALLA.blit(proyectil.imagen, proyectil.rect)

            for enemigo in grupo_enemigos:
                if proyectil.rect.colliderect(enemigo.rect):
                    sonido_muere_enemigo.play()
                    animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados['main'])
                    eliminar_enemigo(enemigo.lados['main'])
                    grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                    proyectil.kill()
                    puntuacion += 70
                    enemigos_eliminados += 1
        if get_mode():
            for lado in personaje.lados:
                pygame.draw.rect(PANTALLA, "Blue", personaje.lados[lado], 2)

            for lado in lados_espada:
                pygame.draw.rect(PANTALLA, "Red", lados_espada[lado], 2)
            for lado in lados_espada_izquierda:
                pygame.draw.rect(PANTALLA, "Red", lados_espada_izquierda[lado], 2)

            for lado in lados_piso:
                pygame.draw.rect(PANTALLA, "Green", lados_piso[lado], 2)

            for lado in lados_plataforma:
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_2[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_3[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_4[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_5[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_6[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_7[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_8[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_9[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_10[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_11[lado], 2)

            for enemigo in grupo_enemigos:
                for lado in enemigo.lados:
                    pygame.draw.rect(PANTALLA, "Cyan", enemigo.lados[lado], 2)

        #BOTON PAUSA
        if pausar_boton.renderizar(PANTALLA):
            retorno = pausa(volumen)
            volumen = retorno['volumen']
            tiempo -= retorno['tiempo_pausa']      
        mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo, vidas, personaje.tiene_escudo)
        pygame.display.flip()

def bucle_de_juego_nivel_3(volumen_parametro = 0.2):
    #MUSICA
    pygame.mixer.music.load(UBICACION_SONIDO_MUSICA_MENU)
    pygame.mixer.music.play(loops=-1)
    volumen = volumen_parametro
    pygame.mixer.music.set_volume(volumen)
    sonido_muere_personaje = pygame.mixer.Sound(UBICACION_SONIDO_RANGER_MUERE)
    sonido_muere_enemigo = pygame.mixer.Sound(UBICACION_SONIDO_ENEMIGO_MUERE)
    #TEXTO
    fuente = pygame.font.SysFont("Arial", 100)
    perdiste_texto = fuente.render("Perdiste!", 0, "Red")
    #FONDO
    fondo = pygame.image.load("fondos/fondo_ciudad.jpg")
    fondo = pygame.transform.scale(fondo, (W,H))
    #FPS
    FPS = 15
    RELOJ = pygame.time.Clock()
    tick = pygame.USEREVENT + 0
    pygame.time.set_timer(tick, 100)
    #PERSONAJE
    personaje = Personaje(H/2 -250, 450, personaje_quieto)
    #PLATAFORMAS
    piso.top = personaje.rect.bottom
    lados_piso = obtener_rectangulos(piso)
    plataforma_1 = Plataforma(580, 460, ("fondos/13.png"))
    plataforma_2 = Plataforma(1080, 460, ("fondos/7.png"))
    plataforma_3 = Plataforma(958, 460, ("fondos/7.png"))
    lados_plataforma = obtener_rectangulos(plataforma_1.rect)
    lados_plataforma_2 = obtener_rectangulos(plataforma_2.rect)
    lados_plataforma_3 = obtener_rectangulos(plataforma_3.rect)
    lista_plataformas = [lados_piso, lados_plataforma, lados_plataforma_2, lados_plataforma_3]
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(plataforma_1, plataforma_2, plataforma_3)
    #ENEMIGO
    grupo_enemigos = Enemigo.generar_enemigos(4)
    #ESPADA
    espada = Espada(H/2 -230, 430, 40)
    rectangulo_espada = pygame.Rect(espada.x,espada.y,espada.z,espada.z)
    rectangulo_espada_izquierda = pygame.Rect(espada.x, espada.y,espada.z,espada.z)
    lados_espada = obtener_rectangulos(rectangulo_espada)
    lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
    #ORBE
    orbe = Orbe(H/2 -250, 390)
    grupo_orbes = pygame.sprite.Group()
    grupo_orbes.add(orbe)
    #PUNTUACION 
    enemigos_eliminados = 0
    nivel = 3
    puntuacion = 0
    tiempo = 180000
    juego_corriendo = True
    vidas = 3
    tiempo_colision = 0
    #BOSS
    boss = Boss()
    boss_lados = obtener_rectangulos(boss.rect)

    while juego_corriendo:
        milisegundos = RELOJ.tick(FPS)
        tiempo -= milisegundos
        if tiempo < 0:
            sonido_muere_personaje.play()
            PANTALLA.blit(fondo_perdiste, (0,0))
            PANTALLA.blit(perdiste_texto, (450, 250))
            pygame.display.flip()
            time.sleep(2)
            perdiste(puntuacion, volumen)
        #EVENTOS 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_corriendo = False
                sys.exit(0)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    retorno = pausa(volumen)
                    volumen = retorno['volumen']
                if evento.key == pygame.K_TAB:
                    cambiar_modo()

        personaje.update()
        rectangulo_espada.x = personaje.rect.x +45
        rectangulo_espada.y = personaje.rect.y
        rectangulo_espada_izquierda.x = personaje.rect.x -45
        rectangulo_espada_izquierda.y = personaje.rect.y 
        lados_espada = obtener_rectangulos(rectangulo_espada)
        lados_espada_izquierda = obtener_rectangulos(rectangulo_espada_izquierda)
        personaje.esta_saltando = False
        orbe.update()
        boss.update()

        if personaje.lados["main"].colliderect(orbe.rect):
            personaje.tiene_escudo = True
            eliminar_enemigo(orbe.lados['main'])
            print("escudo")
            puntuacion += 20

        grupo_plataformas.update()
        grupo_plataformas.draw(PANTALLA)

        for enemigo in grupo_enemigos:
            if personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == False and vidas == 0:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700: 
                    sonido_muere_personaje.play()
                    print("Personaje eliminado!")
                    PANTALLA.blit(fondo_perdiste, (0,0))
                    PANTALLA.blit(perdiste_texto, (450, 250))
                    pygame.display.flip()
                    time.sleep(2)
                    perdiste(puntuacion, volumen)
            elif personaje.lados["main"].colliderect(enemigo.lados["main"]) and personaje.tiene_escudo == True:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    print("ataque bloqueado")
                    personaje.tiene_escudo = False
                    tiempo_colision = 0 
            elif personaje.lados['main'].colliderect(enemigo.lados['main']) and personaje.tiene_escudo == False:
                tiempo_colision += pygame.time.get_ticks() - tiempo_anterior  
                if tiempo_colision >= 700:
                    vidas -= 1
                    tiempo_colision = 0
            elif (personaje.que_hace == "Ataque_derecha" and lados_espada['main'].colliderect(boss.rect)) or (personaje.que_hace == "Ataque_izquierda" and lados_espada_izquierda['main'].colliderect(boss.rect)):
                if boss.delay_proyectil >= boss.DELAY_MAX:
                    boss.colisiones_proyectil += 1
                    boss.delay_proyectil = 0  # Reiniciar el retraso
                    if boss.colisiones_proyectil >= 8:
                        puntuacion += 200
                        sonido_muere_enemigo.play()
                        ganaste(puntuacion, volumen)
                else:
                    boss.delay_proyectil += pygame.time.get_ticks() - boss.delay_proyectil
            elif (personaje.que_hace == "Ataque_derecha" and enemigo.lados["main"].colliderect(rectangulo_espada))or(personaje.que_hace == "Ataque_izquierda" and enemigo.lados["main"].colliderect(rectangulo_espada_izquierda)):
                sonido_muere_enemigo.play()
                animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados["main"])
                eliminar_enemigo(enemigo.lados["main"])
                print("Enemigo eliminado por ataque de espada!")
                grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                puntuacion += 50
                enemigos_eliminados += 1
                if vidas < 3:
                    vidas += 1
            enemigo.update(grupo_plataformas)
            tiempo_anterior = pygame.time.get_ticks()

        actualizar_pantalla_boss(PANTALLA, lista_plataformas, grupo_enemigos, grupo_plataformas, orbe, personaje, boss)

        for proyectil_boss in proyectiles_juego:
            proyectil_boss.update()
            PANTALLA.blit(proyectil_boss.imagen, proyectil_boss.rect)
            if proyectil_boss.rect.colliderect(personaje.rect) and personaje.tiene_escudo == True:
                personaje.tiene_escudo = False
                proyectil_boss.kill()
            if proyectil_boss.rect.colliderect(personaje.rect) and personaje.tiene_escudo == False:
                vidas -= 1
                proyectil_boss.kill()
            if proyectil_boss.rect.colliderect(personaje.rect) and personaje.tiene_escudo == False and vidas == 0:
                sonido_muere_personaje.play()
                print("Personaje eliminado!")
                PANTALLA.blit(fondo_perdiste, (0,0))
                PANTALLA.blit(perdiste_texto, (450, 250))
                pygame.display.flip()
                time.sleep(2)
                perdiste(puntuacion, volumen)
                proyectil_boss.kill()
        boss.disparo()

        for proyectil in proyectiles_juego_personaje:
            proyectil.update()
            PANTALLA.blit(proyectil.imagen, proyectil.rect)
            for enemigo in grupo_enemigos:
                if proyectil.rect.colliderect(enemigo.rect):
                    sonido_muere_enemigo.play()
                    animar_muerte_enemigo(PANTALLA, enemigo_muere, enemigo.lados['main'])
                    eliminar_enemigo(enemigo.lados['main'])
                    grupo_enemigos = Enemigo.agregar_enemigos(grupo_enemigos, 1)
                    proyectil.kill()
                    puntuacion += 70
                    enemigos_eliminados += 1
                if proyectil.rect.colliderect(boss.rect):
                    proyectil.kill()
                    if boss.delay_proyectil >= boss.DELAY_MAX:
                        boss.colisiones_proyectil += 1
                        boss.delay_proyectil = 0 
                        print("Colisiones de proyectil:", boss.colisiones_proyectil)
                        if boss.colisiones_proyectil >= 8:
                            puntuacion += 200
                            sonido_muere_enemigo.play()
                            ganaste(puntuacion, volumen)
                    else:
                        boss.delay_proyectil += pygame.time.get_ticks() - boss.delay_proyectil

        if get_mode():
            for lado in personaje.lados:
                pygame.draw.rect(PANTALLA, "Blue", personaje.lados[lado], 2)

            for lado in lados_espada:
                pygame.draw.rect(PANTALLA, "Red", lados_espada[lado], 2)
            for lado in lados_espada_izquierda:
                pygame.draw.rect(PANTALLA, "Red", lados_espada_izquierda[lado], 2)

            for lado in lados_piso:
                pygame.draw.rect(PANTALLA, "Green", lados_piso[lado], 2)

            for lado in lados_plataforma:
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_2[lado], 2)
                pygame.draw.rect(PANTALLA, "Yellow", lados_plataforma_3[lado], 2)

            for enemigo in grupo_enemigos:
                for lado in enemigo.lados:
                    pygame.draw.rect(PANTALLA, "Cyan", enemigo.lados[lado], 2)

            for lado in orbe.lados:
                pygame.draw.rect(PANTALLA, "Magenta", orbe.lados[lado], 2)
            
            for lado in boss_lados:
                pygame.draw.rect(PANTALLA, "White", boss_lados[lado], 2)

        #BOTON PAUSA
        if pausar_boton.renderizar(PANTALLA):
            retorno = pausa(volumen)
            volumen = retorno['volumen']
            tiempo -= retorno['tiempo_pausa']
        mostrar_resultados(PANTALLA, enemigos_eliminados, puntuacion, nivel, tiempo, vidas, personaje.tiene_escudo)
        pygame.display.flip()