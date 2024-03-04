import pyshark
from pyshark import FileCapture
from pyshark.packet.layers.xml_layer import XmlLayer
from pyshark.packet.packet import Packet
from neo4j import GraphDatabase
from config_data.config import Config, load_config
import logging
import itertools


# Глобальные переменные
cap: FileCapture
pkt: Packet
layer: XmlLayer


class Neo4jWorld: # Класс для работы с Neo4j

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def start_node(self, p_cap : FileCapture):  # Создание нового узла Файл
        with self.driver.session() as session:
            p_cap_node = session.execute_write(self._create_and_return_start_node, p_cap)
            logging.debug("start_node:", p_cap_node)

    @staticmethod
    def _create_and_return_start_node(tx, p_cap : FileCapture):
        logging.debug("Создание стартового узла для файла " + p_cap.input_filepath.name)
        cipher_statement = "CREATE (a:Файл) SET a.file = $name"
        result = tx.run(cipher_statement, name=p_cap.input_filepath.name) # Создаем узел
        return result.single()[0]  # Возвращаем результат оператора CREATE

    def create_packet(self, pcapng_file):  # Создать узел Пакет
        with self.driver.session() as session:
            packet = session.execute_write(self._create_and_return_packet, pcapng_file)
            logging.info(packet)


    @staticmethod  # Создать узел Пакет
    def _create_and_return_packet(tx, message):
        result = tx.run("CREATE (p:Packet) "
                        "SET p.message = $pkt.frame_info. "
                        "RETURN p.message + ', from node ' + id(p)", message=message)
        return result.single()[0]


if __name__ == "__main__":  # Запуск программы
    logging.basicConfig(filename='Wireshark2Neo4j.log',  # Имя файла
                        level=logging.DEBUG,        # Уровень логирования
                        filemode='w')               # Режим логирования
    try:
        config: Config = load_config()  # Загрузка конфигурации из файла .env в переменную config
    except FileNotFoundError:
        logging.error("Не найден файл конфигурации .env")  # Если файл не найден
    try:
        # Создание объекта Neo4jWorld и соединение с базой данных
        pg = Neo4jWorld(config.neo4j_uri,             # uri - адрес Neo4j
                        config.neo4j_creds.user,      # user - имя пользователя Neo4j
                        config.neo4j_creds.password)  # password - пароль пользователя Neo4j
        cap = pyshark.FileCapture(config.file_pcapng)  # Открываем входной файл
        pg.start_node(cap)  # Создаём первый узел графа = входной файл
        for pkt in cap:     # для каждого пакета из файла захвата трафика
            logging.info(pkt)               # Выводим информацию о пакете
            logging.info(pkt.frame_info)    # Выводим информацию о фрейме пакета
            logging.info(pkt.layers)        # Выводим информацию о слоях пакета
            # ToDo: pg.create_packet(pkt)

            i: int = 1
            for layer in pkt.layers:  # для каждого слоя пакета
                logging.info(i, layer)
                i += 1

            # ToDo: Создаем узлы в Neo4j: Пакет, Слой, Источник, Приёмник

        # Закрываем соединение с сервером Neo4j
        pg.close()
    except Exception as e:
        logging.error(e)  # Произошла ошибка
