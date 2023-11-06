import pyshark
from pyshark import FileCapture
from pyshark.packet.layers.xml_layer import XmlLayer
from pyshark.packet.packet import Packet
from neo4j import GraphDatabase
from config_data.config import Config, load_config

cap: FileCapture
pkt: Packet
layer: XmlLayer

class Neo4jWorld:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    def create_packet(self, message):           # Создать узел Пакет
        with self.driver.session() as session:
            packet = session.execute_write(self._create_and_return_packet, message)
            print(packet)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
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
    config: Config = load_config()
    packetgraph = Neo4jWorld("bolt://localhost:7687", config.neo4j_creds.user, config.neo4j_creds.password)
    packetgraph.print_greeting("hello, world")
    packetgraph.close()

    cap = pyshark.FileCapture(r'C:\Users\igorl\OneDrive\Документы\KPM-2.pcapng')
    for pkt in cap:  # для каждого пакета из файла захвата трафика
        print(pkt)
        print(pkt.frame_info)
        print(pkt.layers)
        packetgraph._create_packet(pkt)

        i: int = 1
        for layer in pkt.layers:  # для каждого слоя пакета
            print(i, layer)
            i += 1

        # ToDo: Создаем узлы в Neo4j: Пакет, Слой, Источник, Приёмник
