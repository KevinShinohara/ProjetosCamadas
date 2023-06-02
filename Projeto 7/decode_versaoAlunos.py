
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100 #taxa de amostragem
    tempo = 5
    fs = 44100
    sd.default.channels = 2 #numCanais # o  numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  tempo # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    numAmostras = duration*sd.default.samplerate
    freqDeAmostragem = fs
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("esta gravando")
    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=2)
    sd.wait()
    print("...     FIM")


    data = audio[:,1]
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    divisao = np.linspace(0,5,fs*5)

    plt.figure()
    plt.plot(divisao, data)
    plt.title('dados x tempo')
    plt.show()
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    signal.plotFFT(data,fs)
    plt.show()
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(data, fs)
    print(yf)
    indice = sorted(enumerate(yf), key=lambda x: x[1], reverse=True) [:10]
    print(indice)
    sinal = "erro"

    freq10 = []
    for i in indice:
        valor_x = xf[i[0]]
        valor_y = yf[i[0]]
        print(f"valor_x:{valor_x} e valor_y: {valor_y}")
        freq10.append(valor_x)        
    print(freq10)
    menor = []
    maior = []

    for i in freq10:
        if i < 1000:
            menor.append(i)
        elif i > 1000 and i < 1500:
            maior.append(i)
    
    print(menor)
    print(maior)

    f1 = sum(maior)/len(maior)
    f2 = sum(menor)/len(menor)

    if (f1>1145.5 and f1<=1272.5) :
        if (valor_y >=660.5 and f2 <= 733.5):
            sinal = 1
        elif (f2 >733.5 and f2 <= 811):
            sinal = 4
        elif (f2 >811 and f2 <= 896.5):
            sinal = 7
        elif (f2 >896.5):
            sinal = "X"
    elif(f1>1272.5 and f1<=1406.5):
        if (f2 >=660.5 and f2 <= 733.5):
            sinal = 2
        elif (f2 >733.5 and f2 <= 811):
            sinal = 5
        elif (f2 >811 and f2 <= 896.5):
            sinal = 8
        elif (f2 >896.5):
            sinal = 0
    elif(f1>1406.5 and f1<=1555):
        if (f2 >=660.5 and f2 <= 733.5):
            sinal = 3
        elif (f2 >733.5 and f2 <= 811):
            sinal = 6
        elif (f2 >811 and f2 <= 896.5):
            sinal = 9
        elif (f2 >896.5):
            sinal = "#"
    if(f1>1555):
        if (f2 >=660.5 and f2 <= 733.5):
            sinal = "A"
        elif (f2 >733.5 and f2 <= 811):
            sinal = "B"
        elif (f2 >811 and f2 <= 896.5):
            sinal = "C"
        elif (f2 >896.5):
            sinal = "D"
    print(f"o numumero mandado foi {sinal}")
    


    

    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.4, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
