import socket
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG)

def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))  # IP e porta do servidor
    server_socket.listen(1)

    logging.info("Servidor TCP iniciado em 127.0.0.1:65432")
    
    # Espera por uma conexão
    conn, addr = server_socket.accept()
    logging.info(f"Conexão estabelecida com {addr}")

    with conn:
        with open('received_file_tcp.txt', 'wb') as f:
            while True:
                data = conn.recv(1024)  # Recebe dados de até 1024 bytes
                if not data:
                    break  # Se não houver mais dados, termina a recepção
                f.write(data)  # Escreve os dados no arquivo

        logging.info("Arquivo recebido e salvo como 'received_file_tcp.txt'.")

if __name__ == "__main__":
    start_tcp_server()
