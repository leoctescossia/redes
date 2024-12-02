import socket
import logging
import time  # Para medir o tempo

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

    total_size = 0  # Tamanho total dos dados recebidos
    start_time = None  # Início da transferência

    with conn:
        with open('received_file_tcp.txt', 'wb') as f:
            while True:
                if start_time is None:
                    start_time = time.time()  # Marca o início da transferência
                
                data = conn.recv(1024)  # Recebe dados de até 1024 bytes
                if not data:
                    break  # Se não houver mais dados, termina a recepção
                
                f.write(data)  # Escreve os dados no arquivo
                total_size += len(data)  # Atualiza o tamanho total recebido

    end_time = time.time()  # Marca o final da transferência

    # Calcula estatísticas
    total_time = end_time - start_time
    total_size_mb = total_size / (1024 * 1024)  # Tamanho em megabytes
    bandwidth_mbps = (total_size * 8) / (total_time * 1_000_000)  # Taxa de transferência em Mbps

    logging.info("Arquivo recebido e salvo como 'received_file_tcp.txt'.")
    logging.info(f"Transferência concluída em {total_time:.2f} segundos.")
    logging.info(f"Tamanho total do arquivo: {total_size_mb:.2f} MB.")
    logging.info(f"Taxa de transferência: {bandwidth_mbps:.2f} Mbps.")

if __name__ == "__main__":
    start_tcp_server()
