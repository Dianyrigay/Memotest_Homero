import pygame
import time
import random
import tarjeta
from constantes import *

def crear_tablero():
    '''
    Crea una lista de tarjetas
    Retorna un dict tablero
    '''
    tablero = {}
    lista_tarjetas = generar_lista_tarjetas()
    tablero["tarjetas"] = lista_tarjetas
    tablero["tiempo_ultimo_destape"] = 0
    tablero["primer_tarjeta_seleccionada"] = None
    tablero["segunda_tarjeta_seleccionada"] = None
    return tablero

def generar_lista_ids_tarjetas():
    # Creo una lista con todos los identificadores posibles
    lista_id = list(range(1, CANTIDAD_TARJETAS_UNICAS+1))
    # Extiendo esa lista con otra lista identica ya que hay dos tarjetas iguales en cada tablero (mismo identificador)
    lista_id.extend(list(range(1, CANTIDAD_TARJETAS_UNICAS+1)))
    random.seed(time.time())
    random.shuffle(lista_id)  # Esos identificadores los desordeno de forma al azar
    return lista_id

def generar_lista_tarjetas()->list:
    '''
    Función que se encarga de generar una lista de tarjetas ordenada aleatoriamente
    El for x me recorre todas las posiciones de x usando de step el ancho de la tarjeta
    El for y me recorre todas las posiciones de x usando de step el alto de la tarjeta
    Por ende me va a generar la cantidad de tarjetas que le especifique anteriormente
    ajustandose a la resolución de mi pantalla de manera dinámica
    Usa la función random.shuffle para generar de manera aleatoria los identificadores. Genera una lista de identificadores
    en donde se repiten dos veces el mismo ya que en un memotest se repiten dos veces la misma carta
    Retorna la lista de las tarjetas generadas
    '''
    lista_tarjetas = []
    indice = 0
    lista_id = generar_lista_ids_tarjetas()
    print(lista_id)

    for x in range(0, CANTIDAD_TARJETAS_H * ANCHO_TARJETA, ANCHO_TARJETA):
        for y in range(0, CANTIDAD_TARJETAS_V * ALTO_TARJETA, ALTO_TARJETA):
            nombre_imagen_escondida = "./recursos/00.png"
            tarjeta_creada = tarjeta.crear_tarjeta(
                f"./recursos/0{lista_id[indice]}.png", lista_id[indice], nombre_imagen_escondida, x, y)
            indice+= 1
            lista_tarjetas.append(tarjeta_creada)
    return lista_tarjetas

def detectar_colision(tablero: dict, pos_xy: tuple) -> int  :
    '''
    verifica si existe una colision alguna tarjetas del tablero y la coordenada recibida como parametro
    Recibe como parametro el tablero y una tupla (X,Y)
    Retorna el identificador de la tarjeta que colisiono con el mouse y sino retorna None
    '''
    identificador = None
    for tarjeta in tablero["tarjetas"]:
        if tarjeta["rectangulo"].collidepoint(pos_xy):
            identificador = tarjeta["identificador"]
            if not tarjeta["visible"] and (not tablero["primer_tarjeta_seleccionada"] or not tablero["segunda_tarjeta_seleccionada"]):
                tarjeta["visible"] = True
            if not tablero["primer_tarjeta_seleccionada"]:
                tablero["primer_tarjeta_seleccionada"] = tarjeta
                tablero["tiempo_ultimo_destape"] = pygame.time.get_ticks()
            elif not tablero["segunda_tarjeta_seleccionada"]:
                tablero["segunda_tarjeta_seleccionada"] = tarjeta

    return identificador

def actualizar_tablero(tablero: dict) -> None:
    '''
    Verifica si es necesario actualizar el estado de alguna tarjeta, en funcion de su propio estado y el de las otras
    Recibe como parametro el tablero
    '''
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - tablero["tiempo_ultimo_destape"]

    comparar_tarjetas(tablero)
    if tiempo_transcurrido > TIEMPO_MOVIMIENTO:
        tablero["tiempo_ultimo_destape"] = 0
        for tarjeta in tablero["tarjetas"]:
            if not tarjeta["descubierto"]:
                tarjeta["visible"] = False
        tablero["primer_tarjeta_seleccionada"] = None
        tablero["segunda_tarjeta_seleccionada"] = None

def comparar_tarjetas(tablero: dict) -> bool or None:
    '''
    Funcion que se encarga de encontrar un match en la selección de las tarjetas del usuario.
    Si el usuario selecciono dos tarjetas está función se encargara de verificar si el identificador
    de las mismas corresponde si es así retorna True, sino False.
    En caso de que no hayan dos tarjetas seleccionadas retorna None
    '''
    retorno = None
    if tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None:
        retorno = False
        if tablero["primer_tarjeta_seleccionada"]["identificador"] == tablero["segunda_tarjeta_seleccionada"]["identificador"]:
            tarjeta.descubrir_tarjetas(tablero["tarjetas"], tablero["primer_tarjeta_seleccionada"]["identificador"])
            retorno = True
    return retorno

def dibujar_tablero(tablero: dict, pantalla_juego: pygame.Surface):
    '''
    Dibuja todos los elementos del tablero en la superficie recibida como parametro
    Recibe como parametro el tablero y la ventana principal
    '''
    for tarjeta in tablero["tarjetas"]:
        if tarjeta["visible"]:
            pantalla_juego.blit(tarjeta["superficie"], tarjeta["rectangulo"])
        else:
            pantalla_juego.blit(tarjeta["superficie_escondida"], tarjeta["rectangulo"])
