#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        print("Abriu a comunicação")
        

        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1) 

        lista_de_comandos = []
        #Começando a receber os dados  
        numero_de_comandos = 0
        print("começo")
        while 1:
            primeiro_bit_tamanho = com1.getData(1)
            if primeiro_bit_tamanho[0]== b'\xbb':
                #print("saiu")
                break
            else:
                primeiro_int_tamanho = int.from_bytes(primeiro_bit_tamanho[0], byteorder='big')
                #print(primeiro_int_tamanho)

                
                comando_recebido = com1.getData(primeiro_int_tamanho)
                lista_de_comandos.append(comando_recebido)
                numero_de_comandos += 1
                
        erro = 2 # condição de erro
        arraydebites = bytearray()
        if erro == 1:
            numero_de_comandos += 1
        elif erro == 2:
            time.sleep(5) 
            numero_de_comandos = 0
          

        bite_de_comandos = numero_de_comandos.to_bytes(1, byteorder="big")
        arraydebites += bite_de_comandos
        txBuffer = arraydebites 

        
        print("vou enviar a lista de bytes de tamanho {}".format(numero_de_comandos))

        
        com1.sendData(txBuffer)

        txSize = com1.tx.getStatus()

        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)


        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
        

        
          
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
