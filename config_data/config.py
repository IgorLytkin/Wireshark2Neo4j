from dataclasses import dataclass
from environs import Env


@dataclass
class Neo4jCredentials:
    user: str       # Логин в Neo4j
    password: str   # Пароль в Neo4j


@dataclass
class Config:
    neo4jcreds: Neo4jCredentials


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(neo4jcreds = Neo4jCredentials(user=env('NEO4J_USER'), password=env('NEO4J_PASSWORD')))
