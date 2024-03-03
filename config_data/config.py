from dataclasses import dataclass
from environs import Env


@dataclass
class Neo4jCredentials:
    user: str       # Логин в Neo4j
    password: str   # Пароль в Neo4j


@dataclass
class Config:
    neo4j_uri: str                  # URI сервера Neo4j (например, bolt://localhost:7687)
    neo4j_creds: Neo4jCredentials   # логин и пароль на сервере Neo4j
    file_pcapng: str                # путь к файлу с трафиком в формате .pcapng

# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями neo4j_uri, neo4j_creds (user,password), file_pcapng


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(neo4j_uri=env('NEO4J_URI'),
                  neo4j_creds=Neo4jCredentials(user=env('NEO4J_USER'), password=env('NEO4J_PASSWORD')),
                  file_pcapng=env('FILE_PCAPNG'))
