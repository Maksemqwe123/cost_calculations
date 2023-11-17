import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class PostgresConn:
    host: str
    user: str
    password: str
    db_name: str


@dataclass
class ApiOCR:
    api_key: str


@dataclass
class TextEncryption:
    fernet_key: str


@dataclass
class Config:
    tg_bot: TgBot
    db_conn: PostgresConn
    api_ocr: ApiOCR
    text_encryption: TextEncryption


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config['BOT']
    db_conn = config['DATABASE']
    api_ocr = config['API OCR']
    text_encryption = config['TEXT ENCRYPTION']

    return Config(
        tg_bot=TgBot(
            token=tg_bot['TOKEN'],
            admin_id=int(tg_bot['ADMIN_ID'])
        ),
        db_conn=PostgresConn(
            host=db_conn['HOST'],
            user=db_conn['USER'],
            password=db_conn['PASSWORD'],
            db_name=db_conn['DB_NAME']
        ),
        api_ocr=ApiOCR(
            api_key=api_ocr['API_KEY']
        ),
        text_encryption=TextEncryption(
            fernet_key=text_encryption['FERNET_KEY']
        )
    )


if __name__ == '__main__':
    config_ = load_config(r'C:\Service_finance\cost_calculations\config\config.ini')
