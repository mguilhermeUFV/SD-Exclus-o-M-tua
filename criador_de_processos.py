import socket
import time
from datetime import datetime
import threading
import matplotlib.pyplot as plt

# Constantes
HOST_COORDENADOR = '192.168.56.115'  # IP da máquina coordenadora
PORTA_COORDENADOR = 5000  # Porta do coordenador
TAMANHO_BUFFER = 1024  # Tamanho do buffer
TAMANHO_MENSAGEM = 10  # Tamanho fixo das mensagens em bytes
SEPARADOR = '|'  # Separador de campos das mensagens
CONCEDIDO = '2'  # Código da mensagem de GRANT
LIBERADO = '3'  # Código da mensagem de RELEASE

def criar_mensagem(codigo, id_processo, numero_solicitacao):
    mensagem = codigo + SEPARADOR + id_processo + SEPARADOR + numero_solicitacao
    preenchimento = '0' * (TAMANHO_MENSAGEM - len(mensagem))
    return mensagem + preenchimento

def enviar_mensagem(socket, mensagem):
    socket.sendall(mensagem.encode())

def receber_mensagem(socket):
    dados = socket.recv(TAMANHO_BUFFER).decode()
    return dados.strip()

def registrar_no_arquivo(arquivo, mensagem):
    tempo_atual = datetime.now().strftime("%H:%M:%S.%f")
    arquivo.write(f"{tempo_atual} {mensagem}\n")

def solicitar_acesso(id_processo, tempo_espera, qtd_repeticoes):
    print(f"Iniciando processo {id_processo}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST_COORDENADOR, PORTA_COORDENADOR))
        numero_solicitacao = 1  # Número da primeira solicitação
        for _ in range(qtd_repeticoes):
            print(f"Processo {id_processo} enviando solicitação de acesso...")
            mensagem_solicitacao = criar_mensagem('1', str(id_processo).zfill(4), str(numero_solicitacao).zfill(6))
            enviar_mensagem(s, mensagem_solicitacao)

            # Registrar a mensagem enviada
            with open('resultado.txt', 'a') as arquivo:
                registrar_no_arquivo(arquivo, f"Processo {id_processo} enviou a mensagem: {mensagem_solicitacao}")

            print(f"Processo {id_processo} aguardando resposta do coordenador...")
            resposta = receber_mensagem(s)
            print(f"Processo {id_processo} recebeu resposta do coordenador: {resposta}")
            if resposta.startswith(CONCEDIDO):
                print(f"Processo {id_processo} recebeu acesso à região crítica.")
                with open('resultado.txt', 'a') as arquivo:
                    registrar_no_arquivo(arquivo, f"Processo {id_processo} entrou na região crítica.")
                print(f"Processo {id_processo} aguardando {tempo_espera} segundos...")
                time.sleep(tempo_espera)

                # Registrar saída da região crítica
                with open('resultado.txt', 'a') as arquivo:
                    registrar_no_arquivo(arquivo, f"Processo {id_processo} saiu da região crítica.")

                print(f"Processo {id_processo} enviando mensagem de LIBERADO...")
                mensagem_liberado = criar_mensagem(LIBERADO, str(id_processo).zfill(4), str(numero_solicitacao).zfill(6))
                enviar_mensagem(s, mensagem_liberado)

                # Registrar a mensagem enviada
                with open('resultado.txt', 'a') as arquivo:
                    registrar_no_arquivo(arquivo, f"Processo {id_processo} enviou a mensagem: {mensagem_liberado}")
                
            numero_solicitacao += 1  # Incrementa o número da solicitação
            
        print(f"Finalizando o processo {id_processo}.")

qtd_processos = int(input("Digite a quantidade de processos que deseja enviar: "))
tempo_espera = int(input("Digite o tempo de espera em segundos: "))
qtd_repeticoes = int(input("Digite a quantidade de repetições: "))

# Inicie as threads
for id_processo in range(qtd_processos):
    threading.Thread(target=solicitar_acesso, args=(id_processo+1, tempo_espera, qtd_repeticoes)).start()


