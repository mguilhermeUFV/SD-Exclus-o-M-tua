import threading
import socket
import queue

# Constantes
HOST = '192.168.56.115' # IP da máquina coordenadora
PORT = 5000 # Porta para escutar as conexões
BUFFER_SIZE = 1024 # Tamanho do buffer

# Dicionário para manter a contagem de GRANTs por processo
grant_counts = {}

# Fila para armazenar as solicitações de acesso
request_queue = queue.Queue()

# Dicionário para manter o socket de cada processo
sockets = {}

# Lock para garantir o acesso seguro à fila
queue_lock = threading.Lock()

def listen_connections():
    print("Iniciando o thread de conexões...")
    # Cria o socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            print("Esperando por uma conexão...")
            # Aceita a conexão
            conn, addr = s.accept()
            print(f"Conexão aceita de {addr}")
            # Cria uma thread para cada nova conexão
            threading.Thread(target=handle_process, args=(conn, addr)).start()

def handle_process(conn, addr):
    print(f"Manipulando o processo de {addr}")
    # Adiciona o socket na estrutura de dados
    sockets[addr] = conn
    while True:
        print(f"Esperando por uma mensagem de {addr}")
        # Lê a mensagem
        msg = conn.recv(BUFFER_SIZE).decode()
        if not msg:  # Se a mensagem estiver vazia, isso indica que o cliente fechou a conexão.
            print(f"Processo {addr} fechou a conexão.")
            break  # Quebra o loop while.
        print(f"Mensagem recebida de {addr}: {msg}")
        # Aqui, você deve processar a mensagem e agir de acordo
        msg_parts = msg.split('|')
        if msg_parts[0] == '1': # REQUEST
            with queue_lock:
                request_queue.put((addr, msg_parts[1])) # adiciona na fila (endereço, ID do processo)
                print(f"REQUEST de {addr} adicionado à fila")



def distributed_mutex():
    print("Iniciando o algoritmo de exclusão mútua distribuída...")
    # Algoritmo de exclusão mútua
    # Esta função deve monitorar a fila de pedidos e enviar GRANTs quando necessário
    while True:
        with queue_lock:
            if not request_queue.empty():
                addr, process_id = request_queue.get()
                print(f"Enviando GRANT para {addr}")
                sockets[addr].sendall(b'2') # envia GRANT
                if process_id in grant_counts:
                    grant_counts[process_id] += 1
                else:
                    grant_counts[process_id] = 1

def interface():
    print("Iniciando a interface...")
    while True:
        command = input()
        # Aqui, você deve implementar os comandos da interface
        if command == '1': # imprimir a fila de pedidos atual
            with queue_lock:
                print(f"Fila de pedidos atual: {list(request_queue.queue)}")
        elif command == '2': # imprimir quantas vezes cada processo foi atendido
            print(f"Contagem de GRANTs por processo: {grant_counts}")
        elif command == '3': # encerrar a execução
            break

# Inicia as threads
threading.Thread(target=listen_connections).start()
threading.Thread(target=distributed_mutex).start()
threading.Thread(target=interface).start()
