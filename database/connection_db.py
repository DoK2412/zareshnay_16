from sqlmodel import create_engine

import auth


class JobDB(object):

    def __init__(self):
        self.user: str = auth.DataBase["user_db"]
        self.password: str = auth.DataBase["password_db"]
        self.db_name: str = auth.DataBase["name_db"]
        self.host: str = auth.DataBase["host_db"]
        self.port: int = auth.DataBase["port_db"]
        self.cursor = None

    def create(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'


engin = create_engine(JobDB().create(),
                      pool_pre_ping=True,
                      connect_args={
                          "keepalives": 1,
                          "keepalives_idle": 30,
                          "keepalives_interval": 10,
                          "keepalives_count": 5,
                      })

