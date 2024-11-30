import asyncio
import logging
import ssl
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted

logging.basicConfig(level=logging.DEBUG)

def create_quic_configuration():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = ssl.CERT_NONE  # Ignora a verificação do certificado para testes (não recomendado em produção)
    return config

class FileSenderProtocol(QuicConnectionProtocol):
    def __init__(self, quic_connection, file_path):
        super().__init__(quic_connection)
        self.file_path = file_path

    async def send_file(self):
        try:
            with open(self.file_path, 'rb') as f:
                file_data = f.read()
                stream_id = self._quic.get_next_available_stream_id()
                
                # Envia os dados no stream
                self._quic.send_stream_data(stream_id, file_data, end_stream=True)
                logging.info(f"Arquivo '{self.file_path}' enviado com sucesso!")

                # Espera o fechamento da conexão após o envio do stream
                await self.await_stream_close(stream_id)
        except Exception as e:
            logging.error(f"Erro ao enviar arquivo: {e}")

    async def await_stream_close(self, stream_id):
        """Aguarda o fechamento do stream após o envio dos dados."""
        while True:
            # Aguarda eventos de fechamento ou interrupção
            event = await self._loop.create_future()
            self._quic.process_events()
            if self._quic.stream_ended(stream_id):
                break
            await asyncio.sleep(0.1)  # Espera para não bloquear o loop

    async def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            logging.info("Handshake concluído com sucesso.")
        else:
            logging.debug(f"Evento QUIC recebido: {event}")

async def send_file_to_server(file_path):
    config = create_quic_configuration()

    try:
        # Conecta ao servidor
        async with connect('127.0.0.1', 4433, configuration=config) as connection:
            # Cria o protocolo com a conexão QUIC
            protocol = FileSenderProtocol(connection._quic, file_path=file_path)
            await protocol.send_file()
            logging.info("Envio finalizado.")
    except Exception as e:
        logging.error(f"Erro na conexão com o servidor: {e}")

if __name__ == "__main__":
    file_path = "sample_1mb.txt"  # Nome do arquivo a ser enviado
    asyncio.run(send_file_to_server(file_path))
