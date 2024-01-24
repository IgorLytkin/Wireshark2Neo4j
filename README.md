# Wireshark2Neo4j
Анализ трафика из Wireshark в Neo4j
Параметры работы скрипта задаются файлом .env

Для соединения с сервером Neo4j нужно перед запуском скрипта установить ssh-тунель:
start ssh -fNL 7687:localhost:7687 -v -i "...\rsa\ssh_host_rsa_key" user@neo4j_fqdn

Пример файла .env:
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=пароль
FILE_PCAPNG=D:\1\30122023.pcapng
