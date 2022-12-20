from tkinter import * #configuração GUI
import cv2 as cv      #tratamento imagem câmera
import numpy as np    #tratamento de arrays
import math           #operações matemáticas
import imutils        #conversor de video para imagem 
from PIL import Image, ImageTk  #conversor de video para imagem 
import serial         #comunicação Aruino - Python
import time

import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#pyinstaller 

#ser = serial.Serial("COM3",baudrate = 2400, timeout = 1) #iniciando a comunicação serial entre Arduino e Python


# class AnimationPlot:
#     global ax
#     def animate(self, dataList):
#         try:
#             arduinoData_float = retorno_do_angulo   # Convert to float
#             dataList.append(arduinoData_float)              # Add to the list holding the fixed number of points to animate

#         except:                                             # Pass if data point is bad                               
#             pass

#         dataList = dataList[-50:]                           # Fix the list size so that the animation plot 'window' is x number of points
        
#         ax.clear()                                          # Clear last data frame
        
#         self.getPlotFormat()
#         ax.plot(dataList)                                   # Plot new data frame
        

#     def getPlotFormat(self):
#         ax.set_ylim([0, 360])                              # Set Y axis limit of plot
#         ax.set_title("Comportamento PID")                        # Set title of figure
#         ax.set_ylabel("Ângulo (Graus)")                              # Set title of y axis
#         ax.set_xlabel("Tempo (Milisegundos)") 

# def function_grafico():
    
#     dataList = []                                           # Create empty list variable for later use
                                                        
#     fig = plt.figure()                                      # Create Matplotlib plots fig is the 'higher level' plot window
#     ax = fig.add_subplot(111)                               # Add subplot to main fig window
#     realTimePlot = AnimationPlot()
#                                                         # Matplotlib Animation Fuction that takes takes care of real time plot.                                                        # Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
#     #ani = animation.FuncAnimation(fig, realTimePlot.animate, frames=100, fargs=(dataList), interval=100) 
#     fig.savefig('graph.jpg')
def function_grafico():
    pass#fig, ax = plt.subplots()
    
                                        
def iniciar_valor():

    if entrada_valor_proporcional.get()  == '':
        kp.set("P")
    else:
        kp.set(str(entrada_valor_proporcional.get()))

    if entrada_valor_integral.get()  == '':
        ki.set("I")
    else:
        ki.set(str(entrada_valor_integral.get()))

    if entrada_valor_derivada.get()  == '':
        kd.set("D")
    else:
        kd.set(str(entrada_valor_derivada.get()))

def botao_iniciar_parar_video():

    global capture, count   #inicia as variáveis count para controle da desativação da câmera e capture para captura própriamente dita
                            #das imagens via OpenCv
    try:
        count += 1
    except NameError:
        count = 1
    
    aux = count % 2

    if aux == 0:
                            #desativa a captura da camera
        captura(0)
    
    if aux != 0:
                            #ativa a captura da camera
        capture = cv.VideoCapture(0)
        captura(1)

def botao_enviar_funcao(activation_value):  

    global vetor        #inicializa o vetor que contém os valores P, I, D, angulo fornecido pelo usuário, velocidade
                        #do motor fornecida pelo usuário, o valor de leitura da câmera e o valor de ativação do motor
    try:

        iniciar_valor()

        vetor = (entrada_valor_proporcional.get()) + "-" + (entrada_valor_integral.get()) + "-" + (entrada_valor_derivada.get()) + "-" + (entrada_angulacao_desejada.get()) + "-" + "255" + "-" + str(retorno_do_angulo) + "-" + str(activation_value) + "+" #entrada camera
                        #vetor "String" sendo lido através das entradas do usuário e armazenado 
        aux = 0

        if not (0 <= float(entrada_angulacao_desejada.get()) <= 360):
                        #verificando se o valor da angulação está dentro do intervalo 0º - 360º
            aux += 1


        if aux == 0:
            print(vetor)
            #ser.write(vetor.encode())                    
             
            # vetor_ard = vetor.encode('utf-8') 
            # print(vetor_ard)
            # ser.write(vetor_ard)
                       #envio propriemente dito do vetor para o Arduino caso condições acima citadas sejam satisfeitas



    except:
        pass

def botao_parar():

    botao_enviar_funcao(0.0) #envia código de desativação do motor

def captura(activation_value):

    global retorno_do_angulo

    c1x = c1y = c2x = c2y  = 0
 
    ret, frame = capture.read()  #inicializa a captura da câmera

    if activation_value == 1:
        
        hsv  = cv.cvtColor(frame,cv.COLOR_BGR2HSV) #leitura da câmera sendo realizada via filtro hsv

        #Criar mask para localizar uma Blob Origem

        low_Red = np.array([160,110,64]) #Valor em HSV
        up_Red = np.array([179,255,255])
        
        mask1 = cv.inRange(hsv, low_Red,up_Red)

        ###########Criar fitros de threshold para que o programa ache apenas um blob

        #Achar o centro desta blobs
        cnts = cv.findContours(mask1, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            #desenhando a blob
            cv.drawContours(frame,[c],-1,(255,0,0), 3)

            M = cv.moments(c)
            a1 = cv.contourArea(c)

            #cx e cy são as posições x e y dos centroides achados
            
            if a1 > 50:    
                try:
                    
                    c1x = int(M["m10"]/M["m00"])
                    c1y = int(M["m01"]/M["m00"])

                    cv.circle(frame, (c1x,c1y),7,(255,255,255),-1)#Desenhando na tela onde o centroide foi detectado

                except ZeroDivisionError:
                    pass

        #Criando uma segunda Mask para encontrar um segundo Blob
            
        low_Green = np.array([50,120,74])
        up_Green = np.array([80,255,255])

        mask2 = cv.inRange(hsv, low_Green,up_Green)

        cnts2 = cv.findContours(mask2, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cnts2 = imutils.grab_contours(cnts2)

        for d in cnts2:
            #desenhando a blob
            cv.drawContours(frame,[d],-1,(255,0,0), 3)
            
            M1 = cv.moments(d)
            a2 = cv.contourArea(d)
            
            if a2 > 50: 
                try:
                #cx e cy são as posições x e y dos centroides achados
                    c2x = int(M1["m10"]/M1["m00"])
                    c2y = int(M1["m01"]/M1["m00"])


                    cv.circle(frame, (c2x,c2y),7,(255,255,255),-1)#Desenhando na tela onde o centroide foi detectado

                except ZeroDivisionError:
                    pass
            #calcular ângulo entre retas
                #P1 é a Origem, então P1 = 00
                #P2 é C2-C1
        try:
            
            p2x = c2x - c1x
            p2y = c2y - c1y
            
            retorno_do_angulo = 180 + math.degrees(math.atan2(p2x,p2y)) 

        except ZeroDivisionError:
            pass
        
        linha = cv.line(frame,(c1x,c1y),(c2x,c2y),(255,0,0),3)

        linha = imutils.resize(linha,width=420)
        im = Image.fromarray(linha)
        retorno_camera = ImageTk.PhotoImage(image=im)

        video.configure(image=retorno_camera)
        video.image = retorno_camera

        try:
            aux1 = vetor[-4]
            if str(aux1) != 'None':           

                if aux1 == '1':
                    botao_enviar_funcao(1.0)
                else:
                    botao_enviar_funcao(0.0)
        except:
            pass

        try:
            function_grafico()
            grafico.configure(image='graph.jpg')
            grafico.image = 'graph.jpg'
        except:
            pass

        video.after(1,lambda: captura(1))
        
    if activation_value == 0:

        capture.release()
        cv.destroyAllWindows()

def janela():

    global grafico, entrada_angulacao_desejada, entrada_valor_proporcional, entrada_valor_proporcional, entrada_valor_integral, entrada_valor_derivada, video, kp, ki, kd

    ########################### JANELA CONFIG ###########################    
    window = Tk()     

    window.geometry("1280x720")

    window.title("GUI TREINAMENTO PID")

    window.configure(bg = "#ffffff")

    canvas = Canvas(window, bg = "#ffffff", height = 720, width = 1280, bd = 0, highlightthickness = 0, relief = "ridge")

    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"background.png")

    canvas.create_image(638, 376, image=background_img)

    ########################### BOTÕES CONFIG ###########################

    imagem_botao_parar_motor = PhotoImage(file = f"parar_motor.png")
    botao_parar_motor = Button(image = imagem_botao_parar_motor, borderwidth = 0, highlightthickness = 0, command = botao_parar, relief = "flat")

    imagem_botao_enviar = PhotoImage(file = f"enviar.png")
    botao_enviar = Button(image = imagem_botao_enviar, borderwidth = 0, highlightthickness = 0, command = lambda: botao_enviar_funcao(1.0), relief = "flat")

    imagem_botao_gravar = PhotoImage(file = f"gravar.png")
    botao_video = Button(image = imagem_botao_gravar, borderwidth = 0, highlightthickness = 0, command = botao_iniciar_parar_video, relief = "flat")

    botao_parar_motor.place(x = 100, y = 619, width = 155, height = 51)
    botao_enviar.place(x = 300, y = 619, width = 155, height = 51)
    botao_video.place(x = 200, y = 430, width = 155, height = 51)

    video = Label(window)
    video.place(x=59, y=110, width=420, height=300)

    grafico = Label(window)
    grafico.place(x = 580, y = 100, width = 670, height = 275)

    ########################### ENTRADAS CONFIG ###########################

    set_font=('Times New Roman', 40)

    ######### VELOCIDADE DO MOTOR #########

    #entrada_velocidade_motor = Entry(bd = 0, bg = "#393939", highlightthickness = 0, font=set_font)
    #entrada_velocidade_motor.place(x = 137, y = 428, width = 261, height = 63)

    ######### ANGULAÇÃO DESEJADA #########

    entrada_angulacao_desejada = Entry(bd = 0, bg = "#393939", highlightthickness = 0, font=set_font)
    entrada_angulacao_desejada.place(x = 137, y = 534, width = 261, height = 63)

    ######### VALOR PROPORCIONAL(P) #########

    entrada_valor_proporcional = Entry(bd = 0, bg = "#393939", highlightthickness = 0, font=set_font)
    entrada_valor_proporcional.place(x = 548, y = 619, width = 242, height = 63)

    ######### VALOR INTEGRAL(I) #########

    entrada_valor_integral = Entry(bd = 0, bg = "#393939", highlightthickness = 0, font=set_font)
    entrada_valor_integral.place(x = 792, y = 619, width = 242, height = 63)

    ######### VALOR DERIVADA(D) #########

    entrada_valor_derivada = Entry(bd = 0, bg = "#393939", highlightthickness = 0, font=set_font)
    entrada_valor_derivada.place(x = 1035, y = 619, width = 241, height = 63)

    kp = StringVar(window)
    ki = StringVar(window)
    kd = StringVar(window)

    if entrada_valor_proporcional.get()  == '':
        kp.set("P")
    else:
        kp.set(str(entrada_valor_proporcional.get()))

    if entrada_valor_integral.get()  == '':
        ki.set("I")
    else:
        ki.set(str(entrada_valor_integral.get()))

    if entrada_valor_derivada.get()  == '':
        kd.set("D")
    else:
        kd.set(str(entrada_valor_derivada.get()))

    saida_user_p = Label(window,textvariable = kp, width=16)
    saida_user_p.place(x = 647, y = 480, width = 30, height = 20)

    saida_user_i = Label(window,textvariable = ki, width=16)
    saida_user_i.place(x = 969, y = 480, width = 30, height = 20)

    saida_user_d = Label(window,textvariable = kd, width=16)
    saida_user_d.place(x = 1118, y = 480, width = 30, height = 20)

    window.resizable(False, False) 
    window.mainloop()

janela()
