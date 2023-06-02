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
        
        #Codigo Predro

        com1.enable()
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1) 

        Error = False

        lista_de_comandos = []
        #Começando a receber os dados  
        numero_de_comandos = 1
        print("começo")

        tudo_certo = False
        confirmacao = b'\x00'
        Pacote_de_confimarcao = bytearray()
        header_Server =  b'\x00'*11
        eop_Server = b'\xbb\xbb\xbb'
        Pacote_de_confimarcao =  header_Server + confirmacao + eop_Server
        
        ### HANDSHAKE




        rxBufferHeader, nRx = com1.getData(15)
        handShake = rxBufferHeader[11]
        if handShake == 1:
            confirmacao = b'\x01'
            print("HandShakado")
            Pacote_de_confimarcao =  header_Server + confirmacao + eop_Server
            com1.sendData(Pacote_de_confimarcao)
            tudo_certo=True
        else:
            tudo_certo = False

        imagem = bytearray()
        Contagem_Pacotes = 1
        while tudo_certo:

            header = 12
            eop = 3
            #pegar informacoes no header#
            header_bytes,header_int = com1.getData(header)
            quantidade_total = header_bytes[0:4]
            tamanho_do_payload = header_bytes[4:8]
            numero_do_pacote = header_bytes[8:12]
            numero_do_pacote_int = int.from_bytes(numero_do_pacote, byteorder='big')
            quantidade_total_int = int.from_bytes(quantidade_total, byteorder='big')


            
            tamanho_int_payload = int.from_bytes(tamanho_do_payload, byteorder='big')
            
            payload_bytes,payload_int = com1.getData(tamanho_int_payload)
            imagem += payload_bytes

            eop_bytes,eop_int = com1.getData(eop)


            # ERRO HARDCODE
            erro = 2
            if erro == 1 :
                numero_do_pacote_int +=1
            if erro ==2 :
                tamanho_int_payload +=1
        
            

            
            if eop_bytes == b'\xbb\xbb\xbb' and numero_do_pacote_int  == Contagem_Pacotes and tamanho_int_payload == len(payload_bytes):
                tudo_certo = True
                confirmacao = b'\x02'
                Pacote_de_confimarcao =  header_Server + confirmacao + eop_Server
                com1.sendData(Pacote_de_confimarcao)
                print(f'Recebido Pacote de Número: {numero_do_pacote_int}')
                print("*---*"*7)
                Contagem_Pacotes+=1
                if numero_do_pacote_int == quantidade_total_int:
                    tudo_certo = False

            elif tamanho_int_payload != len(payload_bytes):
                confirmacao = b'\x03'
                tudo_certo = False
                Pacote_de_confimarcao =  header_Server + confirmacao + eop_Server

                print(f'Tamanho do Pacote é Incorreto')
                com1.sendData(Pacote_de_confimarcao)
                Error = True

            else:
                confirmacao = b'\x00'
                Pacote_de_confimarcao =  header_Server + confirmacao + eop_Server
                tudo_certo = False
                print(f'Problema ao receber o Pacote ')
                com1.sendData(Pacote_de_confimarcao)
                Error = True

            
                
       # erro = 0 # condição de erro
        #arraydebites = bytearray()
        #if erro == 1:
        #    numero_de_comandos += 1
        #elif erro == 2:
        #    time.sleep(5) 
         #   numero_de_comandos = 0


        if Error:
            raise Exception("Houve Erro de Conexão")


        




        imagemW = "recebida.png"



        
        for i in range(len(imagem)):
            print("recebeu {}" .format(imagem[i]))
        f = open(imagemW,'wb')
        f.write(imagem)
        f.close()


        
          
    
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
