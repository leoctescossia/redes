import logging
import asyncio
import time  # Para medir o tempo

from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, ConnectionTerminated

logging.basicConfig(level=logging.DEBUG)

def create_quic_configuration():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    return config

class FileReceiverProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received_data = b''  # Buffer para dados recebidos
        self.start_time = None    # Início da transferência
        self.end_time = None      # Fim da transferência

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            if self.start_time is None:  # Marca o início do tempo na primeira mensagem
                self.start_time = time.time()
                logging.info("Transferência iniciada.")

            logging.info(f"Dados recebidos no stream {event.stream_id}: {len(event.data)} bytes.")
            self.received_data += event.data  # Adiciona os dados ao buffer
            
            if event.end_stream:  # O stream foi encerrado
                self.end_time = time.time()
                self.save_received_file()
                self.calculate_transfer_stats()

        elif isinstance(event, ConnectionTerminated):
            logging.info("Conexão QUIC terminada.")

    def save_received_file(self):
        if self.received_data:
            with open('received_file', 'wb') as f:
                f.write(self.received_data)
            logging.info("Arquivo recebido e salvo como 'received_file'.")
        else:
            logging.warning("Nenhum dado recebido para salvar.")

    def calculate_transfer_stats(self):
        if self.start_time and self.end_time:
            total_time = self.end_time - self.start_time  # Tempo em segundos
            total_size = len(self.received_data)  # Tamanho em bytes
            total_size_mb = total_size / (1024 * 1024)  # Tamanho em megabytes

            # Calcula a taxa de transferência em Mbps
            bandwidth_mbps = (total_size * 8) / (total_time * 1_000_000)

            logging.info(f"Transferência concluída em {total_time:.2f} segundos.")
            logging.info(f"Tamanho total do arquivo: {total_size_mb:.2f} MB.")
            logging.info(f"Taxa de transferência: {bandwidth_mbps:.2f} Mbps.")

async def serve_quic():
    config = create_quic_configuration()

    try:
        server = await serve(
            '127.0.0.1', 4433, configuration=config, create_protocol=FileReceiverProtocol
        )
        logging.info("Servidor QUIC iniciado em 127.0.0.1:4433")

        # Mantém o servidor ativo
        await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor QUIC: {e}")

if __name__ == "__main__":
    asyncio.run(serve_quic())
import logging
import asyncio
import time  # Para medir o tempo

from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, ConnectionTerminated

logging.basicConfig(level=logging.DEBUG)

def create_quic_configuration():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    return config

class FileReceiverProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received_data = b''  # Buffer para dados recebidos
        self.start_time = None    # Início da transferência
        self.end_time = None      # Fim da transferência

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            if self.start_time is None:  # Marca o início do tempo na primeira mensagem
                self.start_time = time.time()
                logging.info("Transferência iniciada.")

            logging.info(f"Dados recebidos no stream {event.stream_id}: {len(event.data)} bytes.")
            self.received_data += event.data  # Adiciona os dados ao buffer
            
            if event.end_stream:  # O stream foi encerrado
                self.end_time = time.time()
                self.save_received_file()
                self.calculate_transfer_stats()

        elif isinstance(event, ConnectionTerminated):
            logging.info("Conexão QUIC terminada.")

    def save_received_file(self):
        if self.received_data:
            with open('received_file', 'wb') as f:
                f.write(self.received_data)
            logging.info("Arquivo recebido e salvo como 'received_file'.")
        else:
            logging.warning("Nenhum dado recebido para salvar.")

    def calculate_transfer_stats(self):
        if self.start_time and self.end_time:
            total_time = self.end_time - self.start_time  # Tempo em segundos
            total_size = len(self.received_data)  # Tamanho em bytes
            total_size_mb = total_size / (1024 * 1024)  # Tamanho em megabytes

            # Calcula a taxa de transferência em Mbps
            bandwidth_mbps = (total_size * 8) / (total_time * 1_000_000)

            logging.info(f"Transferência concluída em {total_time:.2f} segundos.")
            logging.info(f"Tamanho total do arquivo: {total_size_mb:.2f} MB.")
            logging.info(f"Taxa de transferência: {bandwidth_mbps:.2f} Mbps.")

async def serve_quic():
    config = create_quic_configuration()

    try:
        server = await serve(
            '127.0.0.1', 4433, configuration=config, create_protocol=FileReceiverProtocol
        )
        logging.info("Servidor QUIC iniciado em 127.0.0.1:4433")

        # Mantém o servidor ativo
        await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor QUIC: {e}")

if __name__ == "__main__":
    asyncio.run(serve_quic())
