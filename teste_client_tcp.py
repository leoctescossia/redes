import socket
import logging

# Configuração de log
logging.basicConfig(level=logging.DEBUG)

def send_file_via_tcp(file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta-se ao servidor
    client_socket.connect(('127.0.0.1', 65432))  # IP e porta do servidor
    logging.info(f"Conectado ao servidor em 127.0.0.1:65432")

    # Envia o arquivo
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024):
            client_socket.sendall(chunk)
            logging.debug(f"Enviado {len(chunk)} bytes.")

    logging.info("Arquivo enviado com sucesso!")
    client_socket.close()

if __name__ == "__main__":
    #TODO indicar qual arquivo será enviado
    file_path = "sample_1mb.txt"  # Caminho do arquivo para enviar
    send_file_via_tcp(file_path)
