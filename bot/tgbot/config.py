import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool
    payment_token: str
    signature: str

@dataclass
class Support:
    channel_id: str

@dataclass
class Rasa:
    log_channel_id: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    rasa: Rasa
    support: Support

def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    rasa = config["rasa"]
    support = config["support"]
    
    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
            use_redis=cast_bool(tg_bot.get("use_redis")),
            payment_token=tg_bot["payment_token"],
            signature=tg_bot["signature"],
        ),
        db=DbConfig(**config["db"]),
        rasa = Rasa(
            log_channel_id=int(rasa["log_channel_id"])
        ),
        support = Support(
            channel_id=int(support["channel_id"])
        )
    )
