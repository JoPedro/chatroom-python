import socket
import threading

apelido = input("Escolhar um apelido: ")

host = '127.0.0.1'

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, 55555))

clienteUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive():
    while True:
        try:
            message = cliente.recv(1024).decode('utf-8')
            if message == 'APELIDO':
                cliente.send(apelido.encode('utf-8'))
            else:
                print(message)
        except:
            print("Um erro ocorreu.")
            cliente.close()
            break

def write():
    while True:
        message = f'{apelido}: {input("")}'
        cliente.send(message.encode('utf-8'))
        # Enviar para o log de chat UDP
        clienteUDP.sendto(message.encode('utf-8'), (host, 55556))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()