import logging
import asyncio
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

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            logging.info(f"Recebendo dados: {len(event.data)} bytes")
            self.received_data += event.data  # Adiciona os dados recebidos ao buffer

            # Quando o stream termina, salvamos os dados em um arquivo
            if event.end_stream:
                self.save_received_file()

        elif isinstance(event, ConnectionTerminated):
            logging.info("Conexão QUIC terminada")

    def save_received_file(self):
        with open('received_file', 'wb') as f:
            f.write(self.received_data)
        logging.info("Arquivo recebido e salvo como 'received_file'.")

async def serve_quic():
    config = create_quic_configuration()

    try:
        # Criando o servidor QUIC com a classe de protocolo FileReceiverProtocol
        server = await serve(
            '127.0.0.1', 4433, configuration=config, create_protocol=FileReceiverProtocol
        )
        logging.info("Servidor QUIC iniciado em 127.0.0.1:4433")

        # Mantém o servidor ativo indefinidamente
        await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor QUIC: {e}")

if __name__ == "__main__":
    asyncio.run(serve_quic())
