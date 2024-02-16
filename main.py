import pyshark
from pyshark import FileCapture
from pyshark.packet.layers.xml_layer import XmlLayer
from pyshark.packet.packet import Packet
from neo4j import GraphDatabase
from config_data.config import Config, load_config
import itertools
import logging


cap: FileCapture
pkt: Packet
layer: XmlLayer

class Neo4jWorld:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def start_node(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_start_node, message)
            print(greeting)

    def create_packet(self, message):           # Создать узел Пакет
        with self.driver.session() as session:
            packet = session.execute_write(self._create_and_return_packet, message)
            print(packet)

    @staticmethod
    def _create_and_return_start_node(tx, message):
        result = tx.run("CREATE (a:FilePcapng) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    @staticmethod
    def _create_and_return_packet(tx, message):
        result = tx.run("CREATE (p:Packet) "
                        "SET p.message = $pkt.frame_info. "
                        "RETURN p.message + ', from node ' + id(p)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.basicConfig(level=logging.DEBUG) # установка уровня журналирования

    config: Config = load_config()
    pg = Neo4jWorld(config.neo4j_uri, config.neo4j_creds.user, config.neo4j_creds.password)
    pg.start_node(config.file_pcapng)  # Создаём первый узел графа = имя входного файла

    cap = pyshark.FileCapture(config.file_pcapng)
    for pkt in cap:  # для каждого пакета из файла захвата трафика
        print(pkt)
        print(pkt.frame_info)
        print(pkt.layers)
        # ToDo: pg.create_packet(pkt)

        i: int = 1
        for layer in pkt.layers:  # для каждого слоя пакета
            print(i, layer)
            i += 1

        # ToDo: Создаем узлы в Neo4j: Пакет, Слой, Источник, Приёмник

    # Закрываем соединение с сервером Neo4j
    pg.close()
