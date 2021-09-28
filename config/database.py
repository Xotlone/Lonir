import logging

import psycopg2

from config import CONSTANTS

log = logging.getLogger('logger')

class Database:
    def __init__(self, dbname, user, password, host, sslmode='require'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.sslmode = sslmode

        self.database = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
        self.cursor = self.database.cursor()

    def __call__(self, command: str, output: str=None):
        try:
            self.cursor.execute(command)
            self.database.commit()
            log.debug(f'SQL "{command}"\nSUCCESFULLY EXECUTED!')

            if output == 'one':
                out = self.cursor.fetchone()
            elif output == 'all':
                out = self.cursor.fetchall()
            else:
                out = None
            return out

        except psycopg2.ProgrammingError as error:
            self.database.rollback()
            log.critical(error)
            log.info('Rollback success')
            raise error
    
    def prepare(self):
        self('''CREATE TABLE IF NOT EXISTS guilds (
            id BIGINT UNIQUE,
            log_ch_id BIGINT DEFAULT 0,
            warn_limit SMALLINT DEFAULT 3,
            welcome_msg TEXT DEFAULT 'Мы рады приветствовать тебя, {member.name}',
            welcome_ch BIGINT DEFAULT 0,
            goodbye_msg TEXT DEFAULT 'К сожалению {member.name} покинул наш сервер',
            goodbye_ch BIGINT DEFAULT 0,
            economy BOOLEAN DEFAULT TRUE
        );

            CREATE TABLE IF NOT EXISTS users (
            id BIGINT,
            guild_id BIGINT,
            scores BIGINT DEFAULT 0
        );''')

        log.info(f'Database preparing completed!')
    
    def column_names(self, table: str):
        return self(f'''SELECT *
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = N'{table}';''', 'one')

database = Database(*CONSTANTS.DATABASE_SETTINGS.values())