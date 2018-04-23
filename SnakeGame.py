#MecArbok 8bit game by: Eduardo Rasgado Ruiz. Mayo 2017

#importamos modulos a usar
import pygame, sys, random, time

check_errors = pygame.init()
#(6,0)
if check_errors[1] > 0:#checando errores al importar pygame
    print("(!) Se han iniciado {} errores en el programa... saliendo".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Soporte exitosamente cargado :D")
    
#mostrar el display
playSurface = pygame.display.set_mode((720,460)) #el argumento es una tupla que define el tamaño
pygame.display.set_caption("MecArbok 8bit Retro ITI Game")

#Colores del programa
rojo = pygame.Color(255,0,0) #gameover #este argumento es de 3 paramentros R G B (r,g,b)
verde = pygame.Color(0,255,0) #vibora
negro = pygame.Color(0,0,0) #puntuacion
blanco = pygame.Color(255,255,255) #fondo
cafe = pygame.Color(165,42,42) #comida

#Frames por segundo o  FPS

fpsController = pygame.time.Clock()

#variables
snakePos = [100,50]#poscicion de inicio
snakeBody = [[100,50],[90,50],[80,50]] #las coordenadas en x y y que delimitan en tres listas el cuerpo de la vibora

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]   #las coordenadas en x 
# -y- y deben de aparecer por sorteo y eso es con la libreria random
foodSpawn = True 

direccion = 'DERECHA' #aqui se guarda el estado anterior del movimiento
cambiar_a = direccion #asignacion de estado actual del desplazamiento
score = 0

#funcion de GAMEOVER! y SCORE
def gameOver():
    miFuente = pygame.font.SysFont('monaco',72)     #llamamos la fuente monaco y el tamaño 42
    GOsurf = miFuente.render('Juego Terminado!', True, rojo)   # aqui metemos el string, el antialising y el color
    GOrect = GOsurf.get_rect()      #esta funcion mete el render en un rectangulo
    GOrect.midtop = (360,15)   #posiciona el rectangulo en el centro e coordenadas x=360, y=15
    playSurface.blit(GOsurf,GOrect)     #esto mostara en el display el game over
    showScore(0) #llama a score con choice == 0
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()#salir de la consola
    sys.exit()  #salir de python

def showScore(choice = 1):
    sFuente = pygame.font.SysFont('monaco',34)
    Ssurf = sFuente.render("Puntuación: {}".format(score), True,negro) #el score en pantalla
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (80,10) #definiendo la posicion del score
    else:
        Srect.midtop = (360,120) #score para el gameover
    playSurface.blit(Ssurf,Srect)
    
#Principal logica del juego, usamos un loop infinito:
while True: 
    for event in pygame.event.get(): #eventos del juego, procesamos a cada momento el requerimiento de valores
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):  #  wasd <--Este bloque proporciona los controles
                cambiar_a = 'DERECHA'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                cambiar_a = 'IZQUIERDA'
            if event.key == pygame.K_UP or event.key == ord('w'):
                cambiar_a = 'ARRIBA'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                cambiar_a = 'ABAJO'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT)) #creando un evento para salir
            
    #Validacion de la direccion de la serpiente(evitar cambios direccionales contrarios)
    if cambiar_a == 'DERECHA' and not direccion == 'IZQUIERDA':
        direccion = 'DERECHA'
    if cambiar_a == 'IZQUIERDA' and not direccion == 'DERECHA':
        direccion = 'IZQUIERDA'
    if cambiar_a == 'ARRIBA' and not direccion == 'ABAJO':
        direccion = 'ARRIBA'
    if cambiar_a == 'ABAJO' and not direccion == 'ARRIBA':
        direccion = 'ABAJO'
    
    #definiendo las acciones de los controles en las fisicas del juego movimiento en [x,y]
    if direccion == 'DERECHA':
        snakePos[0] += 10 #avanza 10 bytes de su poscicion a la derecha
    if direccion == 'IZQUIERDA':
        snakePos[0] -= 10
    if direccion == 'ARRIBA':
        snakePos[1] -= 10
    if direccion == 'ABAJO':
        snakePos[1] += 10
        
    #Mecanismo de la vibora: [][][]-->[][]-->[][][]-->[][]-->[][][]--> Sssss! :v
    snakeBody.insert(0,list(snakePos)) #insertamos la nueva poscicion al cuerpo de la snake
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False #Comida no están en pantalla
    else:
        snakeBody.pop()
    #reaparecimiento de la comida
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10] #Sortear el respawneo de nueva comida  
        foodSpawn = True #La comida esta en pantalla
    
    playSurface.fill(blanco) #cambiar el color del background en RGB,con  draw rect rellenamos un rectangulo con color
    for pos in snakeBody:  #X,Y Tamaño de ambos:Rect(x,y,sizex,sizey)
        pygame.draw.rect(playSurface,verde,pygame.Rect(pos[0],pos[1],10,10))  
    
    pygame.draw.rect(playSurface,cafe,pygame.Rect(foodPos[0],foodPos[1],10,10)) #dibujamos la comida
    
    if snakePos[0] > 710 or snakePos[0] < 0:  #Si la cabeza toca los bordes se acaba el juego
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()
    for block in snakeBody[1:]: #Si la cabeza choca con el cuerpo se acaba el juego
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    showScore() #Se muestra el score en pantalla de juego
    pygame.display.flip() #activar el color del fondo
    fpsController.tick(15) #cambiamos el reloj a 25 fps
    
    
    
    
        
            


    
    