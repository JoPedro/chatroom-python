import threading
import socket

host = '127.0.0.1' # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverUDP.bind((host, 55556))

clientes = []
apelidos = []

# Log de todas as mensagens enviadas visível apenas para o servidor
def chatlogUDP():
    while True:
        data,addr = serverUDP.recvfrom(1024)
        print(data.decode('utf-8'))

receive_thread = threading.Thread(target=chatlogUDP)
receive_thread.start()

def broadcast(message):
    for cliente in clientes:
        cliente.send(message)

def handle(cliente):
    while True:
        try:
            message = cliente.recv(1024)
            broadcast(message)
        except:
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apelido = apelidos[index]
            broadcast(f'{apelido} saiu do chat.'.encode('utf-8'))
            apelidos.remove(apelido)
            break

def receive():
    while True:
        cliente, endereco = server.accept()
        print(f'Conectado com {str(endereco)}')

        cliente.send('APELIDO'.encode('utf-8'))
        apelido = cliente.recv(1024).decode('utf-8')
        apelidos.append(apelido)
        clientes.append(cliente)

        print(f'Apelido do cliente é {apelido}.')
        broadcast(f'{apelido} entrou no chat.'.encode('utf-8'))
        cliente.send('Conectado ao servidor.'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()

print("Servidor está escutando...")
receive()