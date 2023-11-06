import pyshark
from pyshark import FileCapture
from pyshark.packet.layers.xml_layer import XmlLayer
from pyshark.packet.packet import Packet

cap: FileCapture
pkt: Packet
layer: XmlLayer

cap = pyshark.FileCapture(r'C:\Users\igorl\OneDrive\Документы\KPM-2.pcapng', use_ek=True)
for pkt in cap:  # для каждого пакета из файла захвата трафика
    print(pkt)
    print(pkt.layers)
    i: int = 1
    for layer in pkt.layers:  # для каждого слоя пакета
        print(i,layer)
        i += 1



        # ToDo: Создаем узлы в Neo4j: Пакет, Слой, Источник, Приёмник
